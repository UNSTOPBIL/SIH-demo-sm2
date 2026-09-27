import json
import os
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from backend.engine.recommender import recommend_packaging, load_seed_commodities
from backend.engine.compliance import get_compliance_details
from backend.engine.pdf_generator import generate_packaging_readiness_pdf

app = FastAPI(
    title="SIH26236 AI Food Packaging Recommendation System",
    description="MoFPI PMFME/ODOP Decision Support System with India Statutory Compliance Shield (FSSAI, BIS, EPR)",
    version="1.0.0"
)

# Enable CORS for local Vite dev server and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecommendRequest(BaseModel):
    commodity_id: str
    commodity_name: Optional[str] = None
    category: Optional[str] = None
    odop_region: Optional[str] = None
    moisture_pct: Optional[float] = Field(None, ge=0.0, le=100.0)
    fat_oil_pct: Optional[float] = Field(None, ge=0.0, le=100.0)
    ph_value: Optional[float] = Field(None, ge=1.0, le=14.0)
    shelf_life_days: Optional[float] = Field(None, ge=1.0, le=3650.0)
    storage_type: Optional[str] = None
    storage_temp_c: Optional[float] = Field(None, ge=-30.0, le=60.0)
    ambient_rh: Optional[float] = Field(None, ge=0.0, le=100.0)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "system": "SIH26236 AI Packaging & Statutory Compliance Engine",
        "ministry": "Ministry of Food Processing Industries (MoFPI)",
        "scheme": "PMFME & ODOP Micro-Enterprise Initiative"
    }

@app.get("/api/commodities")
def list_commodities():
    commodities = load_seed_commodities()
    return {
        "count": len(commodities),
        "commodities": commodities
    }

@app.get("/api/translations")
def get_translations():
    trans_path = os.path.join(os.path.dirname(__file__), "data", "translations.json")
    if os.path.exists(trans_path):
        with open(trans_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

@app.post("/api/recommend")
def get_recommendation(payload: RecommendRequest):
    try:
        result = recommend_packaging(
            commodity_id=payload.commodity_id,
            moisture_pct=payload.moisture_pct,
            fat_oil_pct=payload.fat_oil_pct,
            ph_value=payload.ph_value,
            shelf_life_days=payload.shelf_life_days,
            storage_type=payload.storage_type,
            storage_temp_c=payload.storage_temp_c,
            ambient_rh=payload.ambient_rh
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/compliance/{commodity_id}")
def get_commodity_compliance(
    commodity_id: str,
    ph_value: Optional[float] = None,
    fat_oil_pct: Optional[float] = None,
    moisture_pct: Optional[float] = None,
    commodity_name: Optional[str] = None
):
    try:
        compliance = get_compliance_details(
            commodity_id=commodity_id,
            ph_value=ph_value,
            fat_oil_pct=fat_oil_pct,
            moisture_pct=moisture_pct,
            commodity_name=commodity_name
        )
        return compliance
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/export-pdf")
def export_readiness_pdf(data: Dict[str, Any]):
    try:
        buffer = generate_packaging_readiness_pdf(data)
        commodity_id = data.get("commodity_id", "commodity")
        filename = f"PMFME_Packaging_Compliance_{commodity_id}.pdf"
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
