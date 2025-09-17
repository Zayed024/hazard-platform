#!/usr/bin/env python3
"""
Sample data population script for Synapse Hazard Intelligence Platform
"""

import requests
import json
import time
import random
from datetime import datetime, timedelta

API_BASE = "http://localhost:8000"

# Chennai area coordinates for realistic sample data
CHENNAI_BOUNDS = {
    "lat_min": 12.8,
    "lat_max": 13.3,
    "lon_min": 80.0,
    "lon_max": 80.5
}

SAMPLE_REPORTS = [
    {
        "title": "Heavy flooding on Marina Beach Road",
        "description": "Water level is approximately 2 feet high due to heavy rainfall. Vehicle movement is completely blocked. Several cars are stuck in the water. Emergency services have been notified.",
        "hazard_type": "flood",
        "area": "Marina Beach"
    },
    {
        "title": "Tree fallen across Rajaji Salai",
        "description": "Large banyan tree has fallen due to strong winds during the storm. The tree is completely blocking both lanes of traffic. No injuries reported but traffic is severely affected.",
        "hazard_type": "infrastructure", 
        "area": "Anna Salai"
    },
    {
        "title": "Severe waterlogging in T.Nagar",
        "description": "Heavy rain has caused significant waterlogging near Pondy Bazaar. Water depth is around 1.5 feet. Local shops are affected and pedestrian movement is difficult.",
        "hazard_type": "flood",
        "area": "T.Nagar"
    },
    {
        "title": "Road cave-in near Chennai Central",
        "description": "A portion of the road has caved in creating a dangerous hole approximately 6 feet wide and 4 feet deep. Area has been cordoned off but needs immediate attention.",
        "hazard_type": "infrastructure",
        "area": "Central Station"
    },
    {
        "title": "Electrical wire down in Mylapore",
        "description": "High tension electrical wire has fallen on the road after strong winds. Area is extremely dangerous. TNEB has been informed but wire is still live.",
        "hazard_type": "infrastructure",
        "area": "Mylapore"
    },
    {
        "title": "Flash flooding in Velachery",
        "description": "Sudden flash flooding in low-lying areas of Velachery. Water level rose rapidly within 30 minutes. Several residents evacuated from ground floor apartments.",
        "hazard_type": "flood",
        "area": "Velachery"
    },
    {
        "title": "Bridge damage on ECR",
        "description": "Cracks observed on the flyover bridge on East Coast Road. Heavy trucks are being diverted. Structural engineer assessment needed urgently.",
        "hazard_type": "infrastructure",
        "area": "ECR"
    },
    {
        "title": "Cyclone damage in Besant Nagar",
        "description": "Strong winds have caused significant damage to trees and signboards. Several trees uprooted, power lines affected. Beach road is impassable.",
        "hazard_type": "weather",
        "area": "Besant Nagar"
    },
    {
        "title": "Landslide on Arignar Anna Zoological Park Road",
        "description": "Heavy rains have triggered a small landslide blocking part of the road leading to the zoo. Soil and rocks have spilled onto the carriageway.",
        "hazard_type": "other",
        "area": "Vandalur"
    },
    {
        "title": "Sewer overflow in Adyar",
        "description": "Major sewer line has burst causing overflow on the main road. Unhygienic conditions and foul smell. Health hazard for residents in the vicinity.",
        "hazard_type": "other",
        "area": "Adyar"
    }
]

def generate_random_coordinates():
    """Generate random coordinates within Chennai bounds"""
    lat = random.uniform(CHENNAI_BOUNDS["lat_min"], CHENNAI_BOUNDS["lat_max"])
    lon = random.uniform(CHENNAI_BOUNDS["lon_min"], CHENNAI_BOUNDS["lon_max"])
    return lat, lon

def create_sample_report(report_data):
    """Create a single hazard report"""
    lat, lon = generate_random_coordinates()
    
    report = {
        "title": report_data["title"],
        "description": report_data["description"],
        "hazard_type": report_data["hazard_type"],
        "latitude": lat,
        "longitude": lon,
        "address": f"{report_data['area']}, Chennai, Tamil Nadu, India"
    }
    
    return report

def populate_data():
    """Populate the database with sample hazard reports"""
    print("🌊 Starting Synapse sample data population...")
    print(f"📍 Target area: Chennai, Tamil Nadu")
    print(f"🎯 API endpoint: {API_BASE}")
    
    # Check API health first
    try:
        health_response = requests.get(f"{API_BASE.replace('/api', '')}/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ API server is healthy and responding")
        else:
            print(f"⚠️  API health check returned status {health_response.status_code}")
    except Exception as e:
        print(f"❌ Could not connect to API server: {e}")
        print("   Make sure the backend server is running on http://localhost:8000")
        return
    
    successful_reports = 0
    failed_reports = 0
    
    for i, report_data in enumerate(SAMPLE_REPORTS, 1):
        try:
            report = create_sample_report(report_data)
            
            print(f"\n📋 Creating report {i}/{len(SAMPLE_REPORTS)}: {report['title'][:50]}...")
            
            response = requests.post(f"{API_BASE}/api/hazards/report", 
                                   data=report, 
                                   files=[],
                                   timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                trust_score = result.get('trust_score', 0)
                severity = result.get('estimated_severity', 0)
                
                print(f"   ✅ Created successfully!")
                print(f"   🎯 Trust Score: {trust_score:.2f} | Severity: {severity:.2f}")
                print(f"   📍 Location: {report['latitude']:.4f}, {report['longitude']:.4f}")
                
                successful_reports += 1
            else:
                print(f"   ❌ Failed with status {response.status_code}: {response.text}")
                failed_reports += 1
                
        except Exception as e:
            print(f"   ❌ Error creating report: {e}")
            failed_reports += 1
            
        # Rate limiting to avoid overwhelming the server
        time.sleep(0.5)
    
    print(f"\n🎉 Sample data population complete!")
    print(f"   ✅ Successfully created: {successful_reports} reports")
    print(f"   ❌ Failed: {failed_reports} reports")
    
    if successful_reports > 0:
        print(f"\n🔍 You can now:")
        print(f"   • View the API docs: http://localhost:8000/docs")
        print(f"   • Access the dashboard: http://localhost:3000")
        print(f"   • Check analytics: {API_BASE}/hazards/analytics/dashboard")

def test_api_endpoints():
    """Test various API endpoints"""
    print("\n🧪 Testing API endpoints...")
    
    test_coords = [13.0827, 80.2707]  # Chennai coordinates
    
    endpoints = [
        ("GET", "/health", "Health check"),
        ("GET", "/", "Root endpoint"),
        ("GET", f"/api/hazards/nearby?lat={test_coords[0]}&lon={test_coords[1]}", "Nearby hazards"),
        ("GET", "/api/hazards/analytics/dashboard", "Dashboard analytics")
    ]
    
    for method, endpoint, description in endpoints:
        try:
            url = f"http://localhost:8000{endpoint}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ {description}: OK")
                
                if 'hazards' in data:
                    print(f"      📊 Found {len(data['hazards'])} hazards nearby")
                elif 'total_reports' in data:
                    print(f"      📊 Total reports: {data['total_reports']}")
                    
            else:
                print(f"   ❌ {description}: Status {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {description}: Error - {e}")
            
        time.sleep(0.2)

if __name__ == "__main__":
    print("=" * 60)
    print("🌊 SYNAPSE - Sample Data Population Script")
    print("   AI-Powered Hazard Intelligence Platform")
    print("=" * 60)
    
    try:
        populate_data()
        test_api_endpoints()
        
        print("\n" + "=" * 60)
        print("🚀 Setup complete! Your Synapse platform is ready to use.")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Script interrupted by user")
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        print("   Please check your setup and try again")