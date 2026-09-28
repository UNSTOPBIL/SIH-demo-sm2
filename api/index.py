import os
import sys

# Ensure backend package can be imported from root
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from backend.main import app

# Add root health alias for convenience
@app.get("/")
def root_check():
    return {
        "status": "online",
        "service": "PackAI India Decision Engine",
        "documentation": "/docs",
        "endpoints": [
            "/api/health",
            "/api/commodities",
            "/api/recommend",
            "/api/compliance/{commodity_id}",
            "/api/economics",
            "/api/sustainability",
            "/api/audit-label",
            "/api/audit-samples",
            "/api/verify/{batch_id}",
            "/api/export-pdf"
        ]
    }

# Also ensure /health works at root
@app.get("/health")
def health_alias():
    return {
        "status": "healthy",
        "system": "SIH26236 AI Packaging & Statutory Compliance Engine"
    }
