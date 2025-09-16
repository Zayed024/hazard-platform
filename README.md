# 🌊 Synapse - Integrated Hazard Intelligence Platform

**AI-powered disaster reporting and analysis platform for real-time hazard detection and community safety.**

![Platform](https://img.shields.io/badge/Platform-Cross--Platform-blue)
![Status](https://img.shields.io/badge/Status-MVP--Ready-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen)

## 🎯 Problem Statement

Natural disasters and urban hazards pose significant threats to communities worldwide. Current reporting systems are often:
- **Slow and centralized** - Critical delay in hazard reporting
- **Inaccurate** - No verification mechanism for citizen reports  
- **Language barriers** - Limited accessibility for diverse populations
- **Fragmented** - No unified platform for various hazard types

## 💡 Our Solution

Synapse leverages AI and community intelligence to create a comprehensive, real-time hazard detection and reporting ecosystem.

### 🔧 Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Mobile App     │    │  Web Dashboard  │    │  Admin Portal   │
│  (Flutter)      │    │  (React + TS)   │    │  (React + TS)   │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │     FastAPI Backend     │
                    │   (Python + AI/ML)     │
                    └────────────┬────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                       │                        │
┌───────▼────────┐    ┌─────────▼──────────┐    ┌───────▼────────┐
│  PostgreSQL    │    │      Redis         │    │   External     │
│  + PostGIS     │    │   (Caching)        │    │     APIs       │
│ (Geospatial)   │    │                    │    │ (Weather/Gov)  │
└────────────────┘    └────────────────────┘    └────────────────┘
```

## ✨ Key Features

### 🤖 AI-Powered Intelligence
- **Trust Scoring**: ML algorithms validate report credibility
- **Image Recognition**: Automatic hazard classification from photos
- **Natural Language Processing**: Multi-language support (Hindi, Tamil, Bengali)
- **Sentiment Analysis**: Social media monitoring for early detection

### 🗺️ Geospatial Intelligence  
- **Real-time Mapping**: Interactive hazard visualization
- **Proximity Alerts**: Location-based hazard notifications
- **Cluster Analysis**: Identify hazard patterns and hotspots
- **Route Optimization**: Safe path recommendations

### 📱 Multi-Platform Access
- **Mobile App**: Citizen reporting with GPS and camera integration
- **Web Dashboard**: Command center for emergency responders
- **SMS Gateway**: Accessibility for feature phones
- **API Integration**: Third-party system compatibility

### 🔒 Trust & Verification
- **Community Validation**: Crowd-sourced verification system
- **Official Integration**: Direct links to emergency services
- **Historical Analysis**: Track report accuracy over time
- **Expert Review**: Manual verification for critical incidents

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Flutter SDK 3.0+ (for mobile)
- Git

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-org/synapse-hazard-platform.git
cd synapse-hazard-platform

# Run the quick start script (Windows)
start.bat

# Or manually start services
```

### Option 2: Manual Setup

#### Backend (FastAPI)
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python app/main.py
```

#### Frontend (React)
```bash
cd frontend
npm install
npm start
```

#### Mobile (Flutter)
```bash
cd mobile
flutter pub get
flutter run
```

### Option 3: Docker (Production)
```bash
docker-compose up -d
```

## 📊 Sample Data

Populate the platform with realistic hazard data:

```bash
python scripts/populate_sample_data.py
```

This creates 10 sample hazard reports across Chennai with realistic locations and scenarios.

## 🌐 Access Points

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📸 Screenshots

### Web Dashboard
![Dashboard](docs/images/dashboard.png)
*Real-time hazard intelligence dashboard with interactive map*

### Mobile App
![Mobile](docs/images/mobile-app.png)
*Citizen reporting interface with location and photo capture*

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests  
cd frontend
npm test

# Mobile tests
cd mobile
flutter test
```

## 🔧 Configuration

### Environment Variables
Copy `.env.example` to `.env` and configure:

```env
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/synapse_db
REDIS_URL=redis://localhost:6379

# External APIs
OPENAI_API_KEY=your_openai_key
GOOGLE_MAPS_API_KEY=your_maps_key
TWILIO_ACCOUNT_SID=your_twilio_sid

# Security
JWT_SECRET_KEY=your_secret_key
```

## 📈 Roadmap

See [TODO.md](TODO.md) for detailed development roadmap.

### Phase 1: MVP Foundation ✅
- [x] Basic reporting system
- [x] Web dashboard
- [x] Mobile app
- [x] API foundation

### Phase 2: AI Integration 🔄
- [ ] Trust scoring algorithms
- [ ] Image classification
- [ ] Social media monitoring
- [ ] Multi-language NLP

### Phase 3: Advanced Features 📋
- [ ] Real-time notifications
- [ ] Government API integration
- [ ] Advanced analytics
- [ ] Offline capabilities

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint/Prettier for JavaScript/TypeScript
- Write tests for new features
- Update documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Backend Development**: FastAPI, ML/AI Implementation
- **Frontend Development**: React, Dashboard Design  
- **Mobile Development**: Flutter, Cross-platform
- **DevOps**: Docker, CI/CD, Cloud Deployment
- **Data Science**: ML Models, Analytics

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-org/synapse/issues)
- **Email**: support@synapse-platform.com
- **Discord**: [Join our community](https://discord.gg/synapse)

## 🏆 Acknowledgments

- OpenStreetMap for mapping data
- Material-UI for React components
- Flutter team for mobile framework
- FastAPI for the incredible Python web framework
- The open-source community

---

**Built with ❤️ for safer communities**

*Synapse: Where AI meets community intelligence for disaster resilience.*
