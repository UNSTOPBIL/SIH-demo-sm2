@echo off
setlocal enabledelayedexpansion

echo ======================================================================
echo   SIH26236 - AI Food Packaging Material Recommendation System
echo   Ministry of Food Processing Industries (MoFPI) / PMFME & ODOP Focus
echo ======================================================================
echo.

:: 1. Check Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found in PATH. Please install Python 3.10+
    pause
    exit /b 1
)

:: 2. Check Node
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not found in PATH. Please install Node.js 18+
    pause
    exit /b 1
)

:: 3. Train / Verify Model Artifact
echo [*] Checking AI recommendation model artifact...
if not exist "backend\engine\model.joblib" (
    echo [*] Training Scikit-Learn DecisionTree model on PMFME seed data...
    python backend\engine\train_model.py
) else (
    echo [OK] Verified backend\engine\model.joblib is present.
)

:: 4. Verify Frontend node_modules
if not exist "frontend\node_modules" (
    echo [*] Installing frontend npm dependencies...
    cd frontend
    call npm install
    cd ..
)

:: 5. Launch FastAPI Backend
echo [*] Starting FastAPI Backend on http://127.0.0.1:8000...
start "SIH26236-Backend-FastAPI" cmd /k "python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload"

:: Wait 2 seconds for backend to spin up
timeout /t 2 /nobreak >nul

:: 6. Launch Vite Frontend
echo [*] Starting Vite Frontend on http://localhost:5173...
start "SIH26236-Frontend-Vite" cmd /k "cd frontend && npm run dev"

:: Wait 3 seconds for Vite to bind port
timeout /t 3 /nobreak >nul

:: 7. Launch Browser
echo [*] Opening application in default web browser...
start http://localhost:5173

echo.
echo ======================================================================
echo   [SUCCESS] PackAI System is running!
echo   Frontend:  http://localhost:5173
echo   Backend:   http://127.0.0.1:8000/docs (Swagger OpenAPI UI)
echo.
echo   To stop the application, simply close the two opened terminal windows.
echo ======================================================================
echo.
pause
