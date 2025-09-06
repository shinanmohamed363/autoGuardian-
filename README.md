# AutoGuardian Fuel Management System

🛡️ **AutoGuardian** - An AI-powered fuel efficiency management system that provides intelligent vehicle analysis, ML-based predictions, and personalized recommendations.

## 🚀 Project Overview

AutoGuardian is a comprehensive full-stack web application designed to help users optimize their vehicle's fuel efficiency through advanced machine learning algorithms and AI-powered insights. The system provides detailed fuel consumption analysis, cost calculations, environmental impact assessments, and personalized recommendations.

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Machine Learning Model](#machine-learning-model)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Core Functionality
- **🔐 User Authentication**: Secure JWT-based login/registration system
- **🚗 Vehicle Management**: Add, edit, and manage multiple vehicles
- **📊 Fuel Record Tracking**: Log fuel consumption and track efficiency over time
- **🤖 ML Predictions**: AI-powered fuel consumption predictions using Random Forest
- **🧠 AI Recommendations**: Personalized efficiency tips using Google Gemini AI
- **📈 Analytics Dashboard**: Visual charts and performance metrics
- **📄 PDF Reports**: Generate comprehensive fuel efficiency reports
- **📧 Email Integration**: Send reports via EmailJS

### Advanced Features
- **⭐ Efficiency Rating**: 5-star rating system based on vehicle performance
- **💰 Cost Analysis**: Annual fuel cost calculations and projections
- **🌱 Environmental Impact**: CO2 emissions tracking and analysis
- **📊 Data Visualization**: Interactive charts using Recharts
- **📱 Responsive Design**: Mobile-first responsive UI with Tailwind CSS

## 🛠 Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: JWT (Flask-JWT-Extended)
- **AI Integration**: Google Gemini 2.0 Flash API
- **ML Model**: Random Forest Regression (scikit-learn)
- **API**: RESTful API architecture

### Frontend
- **Framework**: React 19.1.1 with TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Charts**: Recharts
- **PDF Generation**: jsPDF
- **Email**: EmailJS
- **Routing**: React Router DOM

### Machine Learning
- **Model**: Random Forest Regressor
- **Libraries**: scikit-learn, pandas, numpy
- **Features**: Vehicle specifications, engine details, transmission type
- **Output**: Fuel consumption (L/100km), emissions, efficiency rating

## 📁 Project Structure

```
AutoGuardian-FinalProject/
├── autoguardian-fuel-system/
│   ├── backend/                    # Flask backend
│   │   ├── models/                # Database models
│   │   ├── routes/                # API endpoints
│   │   ├── ml_models/             # Machine learning components
│   │   ├── ai_services/           # Google Gemini AI integration
│   │   ├── utils/                 # Utility functions
│   │   └── app.py                 # Flask application entry point
│   └── auto-gardian-frontend/     # React frontend
│       ├── src/
│       │   ├── components/        # React components
│       │   ├── pages/            # Application pages
│       │   ├── services/         # API service layer
│       │   └── App.tsx           # Main React component
│       └── package.json
├── model/
│   └── fuel.ipynb                # Jupyter notebook for ML model training
├── README.md
└── .gitignore
```

## 🚀 Installation

### Prerequisites
- Python 3.7+
- Node.js 16+
- MySQL Database
- Git

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/shinanmohamed363/AutoGuardian-FinalProject_CL_BSCSD_30_48-fullstack.git
   cd AutoGuardian-FinalProject_CL_BSCSD_30_48-fullstack
   ```

2. **Create virtual environment**
   ```bash
   python -m venv fuel_env
   fuel_env\Scripts\activate  # Windows
   # source fuel_env/bin/activate  # macOS/Linux
   ```

3. **Install Python dependencies**
   ```bash
   cd autoguardian-fuel-system/backend
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Create .env file with:
   DATABASE_URL=mysql://username:password@localhost/autoguardian_db
   JWT_SECRET_KEY=your-secret-key
   GOOGLE_API_KEY=your-gemini-api-key
   ```

5. **Run the Flask backend**
   ```bash
   python app.py
   ```

### Frontend Setup

1. **Install Node.js dependencies**
   ```bash
   cd autoguardian-fuel-system/auto-gardian-frontend
   npm install
   ```

2. **Start the React development server**
   ```bash
   npm start
   ```

### Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **AI Insights**: http://localhost:3000/ai-insights/[vehicle-id]

## 🎯 Usage

### Getting Started
1. **Register/Login**: Create an account or login to existing account
2. **Add Vehicle**: Register your vehicle with make, model, year, and specifications
3. **Generate Predictions**: Use ML model to predict fuel efficiency
4. **View AI Insights**: Get personalized recommendations and analysis
5. **Download Reports**: Generate PDF reports or email them
6. **Track Performance**: Monitor fuel consumption over time

### Key Features Usage

#### ML Predictions
```javascript
// Generate fuel efficiency prediction
const prediction = await apiService.generateMLPrediction(vehicleId);
console.log(`Predicted consumption: ${prediction.combined_l_100km} L/100km`);
```

#### AI Recommendations
```javascript
// Get AI-powered recommendations
const recommendations = await apiService.generateAIRecommendations(vehicleId, 'efficiency');
console.log(`AI Suggestion: ${recommendations.recommendations[0].recommendation_text}`);
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/refresh` - Token refresh

### Vehicle Management
- `GET /vehicles` - Get user vehicles
- `POST /vehicles` - Add new vehicle
- `PUT /vehicles/{id}` - Update vehicle
- `DELETE /vehicles/{id}` - Delete vehicle

### ML Predictions
- `POST /predictions` - Generate ML prediction
- `GET /predictions/{vehicle_id}` - Get prediction history
- `GET /predictions/latest/{vehicle_id}` - Get latest prediction

### AI Recommendations
- `POST /recommendations` - Generate AI recommendations
- `GET /recommendations/{vehicle_id}` - Get recommendation history

## 🤖 Machine Learning Model

### Model Details
- **Algorithm**: Random Forest Regression
- **Training Data**: Vehicle specifications and fuel consumption data
- **Features**: Make, model, engine size, cylinders, transmission, fuel type
- **Accuracy**: Optimized for fuel consumption prediction
- **Output**: Combined/Highway/City consumption, emissions, efficiency rating

### Model Training
```python
# Train the model using Jupyter notebook
jupyter notebook model/fuel.ipynb
```

## 📊 Performance Metrics

### System Performance
- **ML Model Response**: <500ms average
- **API Response Time**: <200ms average
- **Frontend Load Time**: <2s initial load
- **Database Queries**: Optimized with indexing
- **Success Rate**: 100% system functionality

## 🔧 Configuration

### Environment Variables
```bash
# Backend (.env)
DATABASE_URL=mysql://user:pass@localhost/db_name
JWT_SECRET_KEY=your-jwt-secret
GOOGLE_API_KEY=your-gemini-api-key
FLASK_ENV=development

# Frontend (.env)
REACT_APP_API_URL=http://localhost:5000
REACT_APP_EMAILJS_SERVICE_ID=service_id
REACT_APP_EMAILJS_TEMPLATE_ID=template_id
REACT_APP_EMAILJS_PUBLIC_KEY=public_key
```

## 🚦 Testing

### Backend Tests
```bash
cd autoguardian-fuel-system/backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd autoguardian-fuel-system/auto-gardian-frontend
npm test
```

### System Tests
```bash
python run_final_tests.py
```

## 📈 Future Enhancements

- [ ] Mobile app development (React Native)
- [ ] Real-time fuel price integration
- [ ] Advanced analytics dashboard
- [ ] Social features and comparisons
- [ ] IoT device integration
- [ ] Multi-language support

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👥 Team

- **Developer**: Shinan Mohamed
- **Student ID**: CL_BSCSD_30_48
- **Institution**: ICBT Campus
- **Program**: BSc (Hons) Software Engineering

## 📄 License

This project is created for academic purposes as part of the final project submission.

## 📞 Support

For support, please contact: shinanmohamed363@gmail.com

---

**🛡️ AutoGuardian** - Drive Smart, Save More, Protect Tomorrow