from fastapi import APIRouter, HTTPException, Depends, UploadFile, File,Form
from typing import List, Optional
from pydantic import BaseModel
import asyncio
from sqlalchemy.orm import Session
from app.database import get_db
from models.hazard import HazardReport
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from sqlalchemy import func, case



from app.ai import text_analyser, image_analyser
from websockets import manager as websocket_manager

router = APIRouter(prefix="/api/hazards", tags=["hazards"])


def calculate_final_trust_score(text_score: float, image_score: float) -> int:
    """Combine scores with weighting."""
    # Weight text more heavily as it provides more context
    final_score = (text_score * 0.65) + (image_score * 0.35)
    return round(final_score,2)



# Save the trust_score to the database with the report
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
async def create_hazard_report(
    # Use Form for multipart data
    title: str = Form(...),
    description: str = Form(...),
    hazard_type: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    address: str = Form(None),
    images: List[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    try:
        if images and len(images) > 3:
            raise HTTPException(status_code=400, detail="Maximum 3 images allowed")


        text_score = text_analyser.analyze_report_text(description)
        image_score = 0.0
        if images:
            image_scores = []
            for image in images:
                image_content = await image.read()
                # It's important to seek back to the start if you need to read the file again
                image.file.seek(0) 
                score = image_analyser.analyze_report_image(image_content)
                image_scores.append(score)
            
            if image_scores:
                image_score = sum(image_scores) / len(image_scores)

        trust_score = calculate_final_trust_score(text_score, image_score)

    # ... logic to upload images to a cloud service ...
        

        location_point = from_shape(Point(longitude, latitude), srid=4326)

        new_report = HazardReport(
            title=title,
            description=description,
            hazard_type=hazard_type,
            latitude=latitude,
            longitude=longitude,
            address=address,
            location=location_point, # Save the geospatial point
            trust_score=trust_score,
            # severity_score can be calculated later or set to a default
            # image_url would be set here after uploading
            
        )
        
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        report_dict = {c.name: getattr(new_report, c.name) for c in new_report.__table__.columns}
        await websocket_manager.broadcast_json(report_dict)
        
    # # Mock trust score calculation
    # trust_score = 0.7 if "flood" in report.description.lower() else 0.5
    
        return {
            "success": True,
            "message": "Hazard report created successfully",
            "report_id": 12345,
            "trust_score": trust_score,
            #"estimated_severity": 0.6
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error processing report: {str(e)}"
        )

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
async def get_dashboard_analytics(db: Session = Depends(get_db)):
    """
    Calculates and returns key statistics for the dashboard.
    """
    # 1. Total Reports
    total_reports = db.query(HazardReport).count()

    # 2. Active Hazards (example: not yet verified)
    active_hazards = db.query(HazardReport).filter(HazardReport.is_verified == False).count()

    # 3. Verified Reports
    verified_reports = db.query(HazardReport).filter(HazardReport.is_verified == True).count()

    # 4. Average Trust Score (handle division by zero)
    avg_trust_score_query = db.query(func.avg(HazardReport.trust_score)).scalar()
    avg_trust_score = round(avg_trust_score_query, 2) if avg_trust_score_query else 0

    # 5. Hazard Type Distribution
    hazard_types_query = db.query(
        HazardReport.hazard_type, 
        func.count(HazardReport.hazard_type)
    ).group_by(HazardReport.hazard_type).all()
    
    hazard_types = {htype: count for htype, count in hazard_types_query}

    return {
        "total_reports": total_reports,
        "active_hazards": active_hazards,
        "verified_reports": verified_reports,
        "avg_trust_score": avg_trust_score,
        "hazard_types": hazard_types
    }