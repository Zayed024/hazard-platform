from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from routes import hazards
from app import websocket_handler
app = FastAPI(
    title="Synapse Hazard Intelligence API",
    description="AI-powered disaster reporting and analysis platform",
    version="0.1.0"
)
app.include_router(hazards.router)
app.include_router(websocket_handler.router)
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(hazards.router)
app.include_router(websocket_handler.router)

@app.get("/")
async def root():
    return {"message": "Synapse API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "synapse-api"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)