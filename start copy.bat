@echo off
echo ====================================
echo 🌊 SYNAPSE - Quick Start Script
echo AI-Powered Hazard Intelligence Platform
echo ====================================
echo.

echo 🚀 Starting all services...
echo.

:: Check if we're in the right directory
if not exist "backend" (
    echo ❌ Error: Please run this script from the project root directory
    echo Expected to find: backend/, frontend/, mobile/ directories
    pause
    exit /b 1
)

:: Start backend server
echo 📡 Starting Backend Server (FastAPI)...
start cmd /k "cd backend && venv\Scripts\activate && python app\main.py"
echo ✅ Backend server starting on http://localhost:8000
timeout /t 2 /nobreak > nul

:: Start frontend development server
echo 🌐 Starting Frontend Dashboard (React)...
start cmd /k "cd frontend && npm start"
echo ✅ Frontend dashboard starting on http://localhost:3000
timeout /t 2 /nobreak > nul

echo.
echo 🎉 All services are starting up!
echo.
echo 📋 Available Services:
echo   • Backend API: http://localhost:8000
echo   • API Docs: http://localhost:8000/docs
echo   • Dashboard: http://localhost:3000
echo   • Health Check: http://localhost:8000/health
echo.
echo 📱 Mobile App:
echo   • Navigate to mobile/ directory
echo   • Run: flutter run (requires Flutter SDK)
echo.
echo 📊 Sample Data:
echo   • Run: python scripts\populate_sample_data.py
echo   • This will populate the API with test hazard reports
echo.
echo ⏹️  To stop services: Close the terminal windows
echo 🔧 For Docker: run "docker-compose up -d"
echo.
pause