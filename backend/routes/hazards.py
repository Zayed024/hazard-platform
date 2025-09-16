from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
import asyncio

router = APIRouter(prefix="/api/hazards", tags=["hazards"])

class HazardReportCreate(BaseModel):
    title: str
    description: str
    hazard_type: str
    latitude: float
    longitude: float
    address: Optional[str] = None
    media_urls: Optional[List[str]] = []

class HazardReportResponse(BaseModel):
    id: int
    title: str
    description: str
    hazard_type: str
    severity_score: float
    trust_score: float
    latitude: float
    longitude: float
    address: str
    is_verified: bool
    created_at: str

@router.post("/report", response_model=dict)
async def create_hazard_report(report: HazardReportCreate):
    # Simulate AI processing
    await asyncio.sleep(0.1)  # Simulate processing time
    
    # Mock trust score calculation
    trust_score = 0.7 if "flood" in report.description.lower() else 0.5
    
    return {
        "success": True,
        "message": "Hazard report created successfully",
        "report_id": 12345,
        "trust_score": trust_score,
        "estimated_severity": 0.6
    }

@router.get("/nearby")
async def get_nearby_hazards(lat: float, lon: float, radius: int = 5000):
    # Mock nearby hazards
    mock_hazards = [
        {
            "id": 1,
            "title": "Road Flooding",
            "hazard_type": "flood",
            "severity_score": 0.8,
            "trust_score": 0.9,
            "latitude": lat + 0.001,
            "longitude": lon + 0.001,
            "distance_meters": 150
        },
        {
            "id": 2,
            "title": "Tree Fall",
            "hazard_type": "infrastructure",
            "severity_score": 0.6,
            "trust_score": 0.7,
            "latitude": lat - 0.002,
            "longitude": lon + 0.002,
            "distance_meters": 280
        }
    ]
    
    return {"hazards": mock_hazards, "total": len(mock_hazards)}

@router.get("/analytics/dashboard")
async def get_dashboard_analytics():
    return {
        "total_reports": 1247,
        "active_hazards": 23,
        "verified_reports": 891,
        "avg_trust_score": 0.73,
        "hazard_types": {
            "flood": 45,
            "infrastructure": 12,
            "weather": 8,
            "other": 15
        }
    }