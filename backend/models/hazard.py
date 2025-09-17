from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean,func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from geoalchemy2 import Geometry

Base = declarative_base()

class HazardReport(Base):
    __tablename__ = "hazard_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    hazard_type = Column(String(50), nullable=False)
    severity_score = Column(Float, default=0.5)
    trust_score = Column(Float, default=0.3)
    report_source = Column(String, default='citizen_app')
    location = Column(Geometry('POINT'))
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(String(500))
    user_id = Column(Integer, nullable=True) # Nullable for social media reports
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    image_url = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
class SocialMediaPost(Base):
    __tablename__ = "social_media_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50))  # twitter, facebook, instagram
    post_id = Column(String(100), unique=True)
    content = Column(Text)
    author = Column(String(100))
    sentiment_score = Column(Float)
    hazard_keywords = Column(String(500))
    location_extracted = Column(String(200))
    created_at = Column(DateTime, server_default=func.now())