import asyncio
import json
import os
import subprocess
import sys
import time
import urllib.request
import websockets

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CDP_PORT = 9222
FRONTEND_URL = "http://127.0.0.1:5173"
BACKEND_HEALTH_URL = "http://127.0.0.1:8000/api/health"

class DOMVisualTester:
    def __init__(self):
        self.backend_proc = None
        self.frontend_proc = None
        self.chrome_proc = None
        self.ws = None
        self.msg_id = 0
        self.console_errors = []
        self.visual_issues = []

    def log(self, msg: str):
        print(f"[DOM-TEST] {msg}", flush=True)

    def start_processes(self):
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        frontend_dir = os.path.join(root_dir, "frontend")

        # 1. Start Backend
        self.log("Starting backend FastAPI on :8000...")
        self.backend_proc = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
            cwd=root_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # 2. Start Frontend Vite
        self.log("Starting frontend Vite server on :5173...")
        self.frontend_proc = subprocess.Popen(
            ["cmd.exe", "/c", "npm", "run", "dev", "--", "--host", "127.0.0.1", "--port", "5173"],
            cwd=frontend_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Wait for backend
        backend_up = False
        for _ in range(30):
            try:
                with urllib.request.urlopen(BACKEND_HEALTH_URL, timeout=1) as res:
                    if res.status == 200:
                        backend_up = True
                        break
            except Exception:
                time.sleep(0.5)

        if not backend_up:
            raise RuntimeError("Backend failed to start on :8000 within 15 seconds")
        self.log("[OK] Backend is alive and healthy on :8000")

        # Wait for frontend
        frontend_up = False
        for _ in range(30):
            try:
                with urllib.request.urlopen(FRONTEND_URL, timeout=1) as res:
                    if res.status == 200:
                        frontend_up = True
                        break
            except Exception:
                time.sleep(0.5)

        if not frontend_up:
            raise RuntimeError("Frontend failed to start on :5173 within 15 seconds")
        self.log("[OK] Frontend is alive and responding on :5173")

        # 3. Start Headless Chrome
        self.log("Starting Headless Chrome with remote debugging on :9222...")
        self.chrome_proc = subprocess.Popen([
            CHROME_PATH,
            "--headless=new",
            f"--remote-debugging-port={CDP_PORT}",
            "--disable-gpu",
            "--no-first-run",
            "--no-default-browser-check",
            "--window-size=1280,900",
            FRONTEND_URL
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1.5)

    async def connect_cdp(self):
        targets_url = f"http://127.0.0.1:{CDP_PORT}/json"
        ws_url = None
        for _ in range(20):
            try:
                with urllib.request.urlopen(targets_url, timeout=1) as res:
                    targets = json.loads(res.read().decode('utf-8'))
                    for t in targets:
                        if t.get('type') == 'page':
                            ws_url = t.get('webSocketDebuggerUrl')
                            break
                    if ws_url:
                        break
            except Exception:
                await asyncio.sleep(0.5)

        if not ws_url:
            raise RuntimeError("Could not find WebSocketDebuggerUrl from Chrome")

        self.log(f"Connecting to Chrome WebSocket: {ws_url}")
        self.ws = await websockets.connect(ws_url)

        # Enable runtime and console
        await self.send_cdp("Runtime.enable")
        await self.send_cdp("Page.enable")
        await self.send_cdp("Console.enable")

    async def send_cdp(self, method: str, params: dict = None) -> dict:
        self.msg_id += 1
        msg = {"id": self.msg_id, "method": method, "params": params or {}}
        await self.ws.send(json.dumps(msg))
        
        while True:
            resp_str = await self.ws.recv()
            data = json.loads(resp_str)
            if data.get("method") == "Runtime.exceptionThrown":
                details = data.get("params", {}).get("exceptionDetails", {})
                exc_text = details.get("text", "")
                exc_desc = details.get("exception", {}).get("description", "")
                self.console_errors.append(f"JS Exception: {exc_text} - {exc_desc}")
            elif data.get("method") == "Console.messageAdded":
                msg_obj = data.get("params", {}).get("message", {})
                if msg_obj.get("level") == "error":
                    self.console_errors.append(f"Console.error: {msg_obj.get('text')}")
            
            if data.get("id") == self.msg_id:
                return data

    async def evaluate(self, expression: str):
        res = await self.send_cdp("Runtime.evaluate", {
            "expression": expression,
            "returnByValue": True,
            "awaitPromise": True
        })
        return res.get("result", {}).get("result", {}).get("value")

    async def inspect_dom(self, screen_name: str, theme: str):
        self.log(f"--- Inspecting [{screen_name}] in [{theme.upper()}] mode ---")

        # 1. Overflow & Horizontal Scroll Check
        overflow_js = """
        (() => {
            const docWidth = document.documentElement.clientWidth;
            const scrollWidth = document.documentElement.scrollWidth;
            const overflows = [];
            document.querySelectorAll('*').forEach(el => {
                if (el.tagName === 'HTML' || el.tagName === 'BODY' || el.tagName === 'SVG' || el.tagName === 'PATH') return;
                const rect = el.getBoundingClientRect();
                if (rect.right > docWidth + 3 && rect.width > 0 && rect.height > 0) {
                    overflows.push({
                        tag: el.tagName.toLowerCase(),
                        className: (typeof el.className === 'string' ? el.className.split(' ').slice(0, 3).join(' ') : ''),
                        width: Math.round(rect.width),
                        right: Math.round(rect.right),
                        docWidth
                    });
                }
            });
            return {
                docWidth,
                scrollWidth,
                hasHorizontalScroll: scrollWidth > docWidth + 1,
                overflowElements: overflows.slice(0, 3)
            };
        })()
        """
        overflow_res = await self.evaluate(overflow_js)
        if overflow_res and overflow_res.get("hasHorizontalScroll"):
            issue = f"Horizontal page overflow detected on [{screen_name}] ({theme}): scrollWidth={overflow_res.get('scrollWidth')} > clientWidth={overflow_res.get('docWidth')}."
            if overflow_res.get("overflowElements"):
                issue += f" Offenders: {overflow_res.get('overflowElements')}"
            self.visual_issues.append(issue)
            self.log(f"  [OVERFLOW] {issue}")
        else:
            self.log(f"  [OK] No horizontal overflow (scrollWidth <= clientWidth)")

        # 2. Text Illegibility & Contrast Check
        contrast_js = """
        (() => {
            const issues = [];
            function parseRgb(colorStr) {
                if (!colorStr) return null;
                const match = colorStr.match(/rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)(?:,\\s*([\\d.]+))?\\)/);
                if (!match) return null;
                return { 
                    r: parseInt(match[1]), 
                    g: parseInt(match[2]), 
                    b: parseInt(match[3]),
                    a: match[4] !== undefined ? parseFloat(match[4]) : 1.0
                };
            }
            function getLuminance(rgb) {
                return 0.299 * rgb.r + 0.587 * rgb.g + 0.114 * rgb.b;
            }
            function getEffectiveBg(el) {
                let curr = el;
                while (curr && curr !== document && curr.nodeType === 1) {
                    const style = window.getComputedStyle(curr);
                    const bg = style.backgroundColor;
                    const rgb = parseRgb(bg);
                    if (rgb && rgb.a > 0.35) {
                        return rgb;
                    }
                    const bgImg = style.backgroundImage || '';
                    if (bgImg.includes('gradient')) {
                        const gradMatch = bgImg.match(/rgb\\((\\d+),\\s*(\\d+),\\s*(\\d+)\\)/);
                        if (gradMatch) {
                            return { r: parseInt(gradMatch[1]), g: parseInt(gradMatch[2]), b: parseInt(gradMatch[3]), a: 1.0 };
                        }
                    }
                    curr = curr.parentElement;
                }
                return document.documentElement.classList.contains('dark') ? {r: 2, g: 6, b: 23, a: 1.0} : {r: 255, g: 255, b: 255, a: 1.0};
            }
            document.querySelectorAll('h1, h2, h3, h4, p, span, button, label, td, th').forEach(el => {
                const text = el.innerText ? el.innerText.trim() : '';
                if (text.length < 3) return;
                // Ignore svg text elements
                if (el.closest('svg')) return;
                const style = window.getComputedStyle(el);
                if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') return;
                const fgRgb = parseRgb(style.color);
                if (!fgRgb) return;
                const bgRgb = getEffectiveBg(el);
                const fgLum = getLuminance(fgRgb);
                const bgLum = getLuminance(bgRgb);
                const diff = Math.abs(fgLum - bgLum);
                if (diff < 22) {
                    issues.push({
                        text: text.substring(0, 30),
                        tag: el.tagName.toLowerCase(),
                        fg: style.color,
                        bg: `rgb(${bgRgb.r},${bgRgb.g},${bgRgb.b})`,
                        diff: Math.round(diff)
                    });
                }
            });
            return issues.slice(0, 5);
        })()
        """
        contrast_res = await self.evaluate(contrast_js)
        if contrast_res and len(contrast_res) > 0:
            for c in contrast_res:
                issue = f"Low contrast text on [{screen_name}] ({theme}): '{c.get('text')}' (tag: {c.get('tag')}, fg: {c.get('fg')}, bg: {c.get('bg')}, lum_diff: {c.get('diff')})"
                self.visual_issues.append(issue)
                self.log(f"  [CONTRAST] {issue}")
        else:
            self.log(f"  [OK] Text contrast & legibility verified across all typography")

        # 3. Unrendered or Broken Elements Check
        broken_js = """
        (() => {
            const broken = [];
            document.querySelectorAll('img').forEach(img => {
                if (img.complete && img.naturalWidth === 0) {
                    broken.push('Broken Image: ' + img.src);
                }
            });
            // Check for React error text in DOM
            const bodyText = document.body.innerText || '';
            if (bodyText.includes('Something went wrong') || bodyText.includes('Cannot read properties of')) {
                broken.push('React crash text present in document body');
            }
            return broken;
        })()
        """
        broken_res = await self.evaluate(broken_js)
        if broken_res and len(broken_res) > 0:
            for b in broken_res:
                self.visual_issues.append(f"Broken element on [{screen_name}] ({theme}): {b}")
                self.log(f"  [BROKEN] Broken element: {b}")
        else:
            self.log(f"  [OK] No broken images or crash boundary messages")

    async def run_suite(self):
        try:
            self.start_processes()
            await self.connect_cdp()

            # Wait for React app to mount
            await asyncio.sleep(2.0)

            # Test across both themes: 'light' and 'dark'
            themes = ['light', 'dark']

            for theme in themes:
                self.log(f"\n==========================================")
                self.log(f"  TESTING IN {theme.upper()} THEME")
                self.log(f"==========================================")

                # Set theme
                if theme == 'dark':
                    await self.evaluate("""
                    (() => {
                        document.documentElement.classList.add('dark');
                        localStorage.setItem('packai_theme', 'dark');
                    })()
                    """)
                else:
                    await self.evaluate("""
                    (() => {
                        document.documentElement.classList.remove('dark');
                        localStorage.setItem('packai_theme', 'light');
                    })()
                    """)
                await asyncio.sleep(0.5)

                # 1. SCREEN 1: Input (Seeded mode)
                await self.evaluate("window.history.pushState({}, '', '/'); window.dispatchEvent(new PopStateEvent('popstate'));")
                await asyncio.sleep(0.5)
                await self.inspect_dom("Screen 1 - Seeded Mode", theme)

                # 2. SCREEN 1: Input (Custom mode)
                await self.evaluate("""
                (() => {
                    const customBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Custom Food Specification'));
                    if (customBtn) customBtn.click();
                })()
                """)
                await asyncio.sleep(0.5)
                await self.inspect_dom("Screen 1 - Custom Mode", theme)

                # Switch back to seeded mode & trigger Analyze
                await self.evaluate("""
                (() => {
                    const seededBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('ODOP / PMFME Database'));
                    if (seededBtn) seededBtn.click();
                })()
                """)
                await asyncio.sleep(0.5)

                # Click "Generate AI Packaging Recommendation"
                self.log("Clicking 'Generate AI Packaging Recommendation'...")
                await self.evaluate("""
                (() => {
                    const analyzeBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Generate AI Packaging Recommendation'));
                    if (analyzeBtn) analyzeBtn.click();
                })()
                """)
                # Wait for ML inference and barrier calculation
                await asyncio.sleep(2.0)

                # 3. SCREEN 2: Recommendation & Kinetics Studio
                await self.inspect_dom("Screen 2 - Recommendation & Kinetics", theme)

                # Click "Proceed to India Statutory Shield"
                await self.evaluate("""
                (() => {
                    const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('India Statutory Shield'));
                    if (nextBtn) nextBtn.click();
                })()
                """)
                await asyncio.sleep(1.0)

                # 4. SCREEN 3: Compliance Studio & Simulant Matrix & FMCG Label
                await self.inspect_dom("Screen 3 - Statutory Compliance & Labelling", theme)

                # Click "Generate 1-Page Readiness Sheet"
                await self.evaluate("""
                (() => {
                    const sheetBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Readiness Sheet'));
                    if (sheetBtn) sheetBtn.click();
                })()
                """)
                await asyncio.sleep(1.0)

                # 5. SCREEN 4: Readiness Sheet Certificate
                await self.inspect_dom("Screen 4 - Packaging Readiness Certificate", theme)

                # 6. DIGITAL PRODUCT PASSPORT (/verify)
                await self.evaluate("window.history.pushState({}, '', '/verify?id=makhana&batch=PMFME-2026-CERT'); window.dispatchEvent(new PopStateEvent('popstate'));")
                await asyncio.sleep(1.5)
                await self.inspect_dom("Digital Product Passport (/verify)", theme)

                # 7. LABEL ARTWORK AUDITOR (/audit)
                await self.evaluate("window.history.pushState({}, '', '/audit'); window.dispatchEvent(new PopStateEvent('popstate'));")
                await asyncio.sleep(1.0)
                await self.inspect_dom("Label Artwork Auditor (/audit)", theme)

                # Test compliant sample audit
                await self.evaluate("""
                (() => {
                    const sampleBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Load Compliant Sample'));
                    if (sampleBtn) sampleBtn.click();
                })()
                """)
                await asyncio.sleep(1.5)
                await self.inspect_dom("Label Auditor - Compliant Result", theme)

                # Test defective sample audit
                await self.evaluate("""
                (() => {
                    const defBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Load Defective Sample'));
                    if (defBtn) defBtn.click();
                })()
                """)
                await asyncio.sleep(1.5)
                await self.inspect_dom("Label Auditor - Defective Result", theme)

            # Final Report
            self.log("\n==========================================")
            self.log("  DOM VISUAL VALIDATION SUMMARY")
            self.log("==========================================")
            self.log(f"Total Console Errors: {len(self.console_errors)}")
            for err in self.console_errors:
                self.log(f"  [ERROR] {err}")
            
            self.log(f"Total Visual DOM Issues: {len(self.visual_issues)}")
            for issue in self.visual_issues:
                self.log(f"  [ISSUE] {issue}")

            if len(self.console_errors) == 0 and len(self.visual_issues) == 0:
                self.log("[PERFECT] DOM VISUAL TEST: 0 errors, 0 overflow issues, 100% legibility in both Light and Dark mode!")
            else:
                self.log(f"[WARN] Found {len(self.console_errors)} errors and {len(self.visual_issues)} visual issues to resolve.")

        finally:
            self.cleanup()

    def cleanup(self):
        self.log("Cleaning up processes...")
        if self.ws:
            try:
                asyncio.run(self.ws.close())
            except Exception:
                pass
        if self.chrome_proc:
            try:
                self.chrome_proc.terminate()
            except Exception:
                pass
        if self.frontend_proc:
            try:
                self.frontend_proc.terminate()
            except Exception:
                pass
        if self.backend_proc:
            try:
                self.backend_proc.terminate()
            except Exception:
                pass
        # Kill any lingering node or chrome processes on these ports if needed
        subprocess.run(["cmd.exe", "/c", "taskkill", "/F", "/IM", "chrome.exe"], capture_output=True)
        self.log("Cleanup complete.")

if __name__ == "__main__":
    tester = DOMVisualTester()
    asyncio.run(tester.run_suite())
