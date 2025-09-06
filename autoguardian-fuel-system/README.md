# AutoGuardian Fuel Management System

A comprehensive web application for vehicle fuel consumption prediction, tracking, and analysis using machine learning and AI-powered recommendations.

## 🚀 Features

### Core Functionality
- **ML-Powered Predictions**: Fuel consumption predictions using Random Forest model
- **Real-time Tracking**: Fuel refill records and odometer tracking
- **AI Recommendations**: Google Gemini AI-powered fuel efficiency tips
- **Advanced Analytics**: Comprehensive reporting and visualizations
- **Multi-vehicle Support**: Manage multiple vehicles per user

### Key Capabilities
- Predict combined, highway, and city fuel consumption
- Track actual vs predicted performance
- Generate personalized fuel-saving recommendations
- Calculate environmental impact and cost projections
- Compare multiple vehicles' efficiency
- Export data for external analysis

## 🛠 Technology Stack

### Backend
- **Framework**: Flask 2.3.3
- **Database**: MariaDB with SQLAlchemy ORM
- **Authentication**: JWT tokens with Flask-JWT-Extended
- **ML/AI**: scikit-learn, Google Generative AI (Gemini)
- **Data Processing**: pandas, numpy

### Frontend (To Be Implemented)
- **Framework**: React 18+ with TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Chart.js/Recharts
- **State Management**: React Context + React Query

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- MariaDB 10.5+
- Node.js 16+ (for frontend)
- Google AI API key (for recommendations)

### Backend Setup

1. **Clone and Navigate**
   ```bash
   cd autoguardian-fuel-system/backend
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration:
   ```
   
   ```env
   # Database Configuration
   DATABASE_URL=mysql+pymysql://root:@127.0.0.1:3306/autoguardian_db
   
   # Flask Configuration
   SECRET_KEY=your-very-secure-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-key-here
   
   # Google AI Integration
   GOOGLE_AI_API_KEY=your-google-gemini-api-key-here
   
   # Optional Configuration
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

5. **Database Setup**
   ```bash
   # Create database using the provided SQL script
   mysql -u root -p < migrations/create_database.sql
   ```

6. **Verify ML Model**
   ```bash
   # Ensure the trained model is in place
   ls ml_models/best_fuel_model_random_forest.pkl
   ```

7. **Run Application**
   ```bash
   python app.py
   ```

   The server will start at `http://localhost:5000`

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile
- `POST /api/auth/change-password` - Change password
- `GET /api/auth/preferences` - Get user preferences
- `PUT /api/auth/preferences` - Update preferences

### Vehicle Management
- `POST /api/vehicles` - Add new vehicle
- `GET /api/vehicles` - Get user's vehicles
- `GET /api/vehicles/<vehicle_id>` - Get specific vehicle
- `PUT /api/vehicles/<vehicle_id>` - Update vehicle
- `DELETE /api/vehicles/<vehicle_id>` - Delete vehicle

### Fuel Records
- `POST /api/fuel-records` - Add fuel record
- `GET /api/fuel-records/<vehicle_id>` - Get vehicle fuel records
- `PUT /api/fuel-records/<id>` - Update fuel record
- `DELETE /api/fuel-records/<id>` - Delete fuel record
- `POST /api/fuel-records/validate-odo` - Validate odometer reading

### ML Predictions
- `POST /api/predictions/predict` - Generate fuel predictions
- `GET /api/predictions/<vehicle_id>` - Get vehicle predictions
- `POST /api/predictions/batch` - Batch predictions for multiple vehicles

### AI Recommendations
- `POST /api/recommendations/generate` - Generate AI recommendations
- `GET /api/recommendations/<user_id>` - Get user recommendations
- `PUT /api/recommendations/<id>/read` - Mark as read
- `PUT /api/recommendations/<id>/implement` - Mark as implemented

### Analytics
- `POST /api/analytics/comprehensive-report/<vehicle_id>` - Generate comprehensive report
- `GET /api/analytics/driving-patterns/<vehicle_id>` - Get driving pattern analysis
- `GET /api/analytics/consumption-trends/<vehicle_id>` - Get consumption trends
- `POST /api/analytics/compare-vehicles` - Compare multiple vehicles

## 🎯 Usage Examples

### 1. User Registration
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123!",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### 2. Add Vehicle
```bash
curl -X POST http://localhost:5000/api/vehicles \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "vehicle_id": "BMW_X5_2023",
    "vehicle_name": "My BMW X5",
    "make": "BMW",
    "model": "X5",
    "year": 2023,
    "vehicle_class": "SUV: SMALL",
    "engine_size": 3.0,
    "cylinders": 6,
    "transmission": "A8",
    "fuel_type": "Z",
    "tank_capacity": 83.0,
    "full_tank_capacity": 83.0,
    "odo_meter_when_buy_vehicle": 10000
  }'
```

### 3. Generate ML Prediction
```bash
curl -X POST http://localhost:5000/api/predictions/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "vehicle_id": "BMW_X5_2023"
  }'
```

### 4. Add Fuel Record
```bash
curl -X POST http://localhost:5000/api/fuel-records \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "vehicle_id": "BMW_X5_2023",
    "record_date": "2025-01-15",
    "record_time": "14:30",
    "existing_tank_percentage": 25,
    "after_refuel_percentage": 100,
    "odo_meter_current_value": 10500,
    "driving_type": "mix",
    "location": "Colombo",
    "fuel_price": 340,
    "notes": "Regular refill"
  }'
```

## 🔬 ML Model Details

### Input Features
- **MAKE**: Vehicle manufacturer (standardized)
- **MODEL**: Vehicle model (standardized)  
- **VEHICLE CLASS**: Vehicle category
- **ENGINE SIZE**: Engine displacement (L)
- **CYLINDERS**: Number of cylinders
- **TRANSMISSION**: Transmission type (A4-A10, M5-M7, AV, AS)
- **FUEL**: Fuel type (X=Regular, Z=Premium, D=Diesel)

### Outputs
- **Combined Consumption**: L/100km for mixed driving
- **Highway Consumption**: L/100km for highway driving
- **City Consumption**: L/100km for city driving
- **CO2 Emissions**: g/km
- **Efficiency Rating**: 1-5 star rating
- **Annual Projections**: Cost and environmental impact

### Feature Preprocessing
The system automatically handles:
- Make/model standardization
- Transmission type mapping
- Fuel type conversion
- Engine size normalization
- Validation and error handling

## 🤖 AI Recommendations

The system uses Google Gemini AI to generate personalized recommendations based on:
- Vehicle performance vs predictions
- Driving patterns and fuel consumption data
- Cost optimization opportunities
- Environmental impact considerations
- Maintenance suggestions

## 🗄 Database Schema

### Key Tables
- **users**: User accounts and authentication
- **user_preferences**: User customization settings
- **vehicles**: Vehicle specifications and metadata
- **fuel_records**: Refueling events and consumption tracking
- **ml_predictions**: Machine learning prediction results
- **ai_recommendations**: AI-generated suggestions
- **vehicle_statistics**: Cached performance metrics

### Relationships
- One user → Many vehicles
- One vehicle → Many fuel records
- One vehicle → Many predictions
- One user → Many recommendations

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt for password security
- **Input Validation**: Comprehensive data validation
- **SQL Injection Protection**: Parameterized queries
- **CORS Configuration**: Controlled cross-origin access
- **Rate Limiting**: API request throttling (configurable)

## 📊 Analytics & Reporting

### Available Analytics
- **Performance Analysis**: Actual vs predicted consumption
- **Driving Pattern Breakdown**: City/highway/mixed analysis
- **Cost Tracking**: Fuel expenses and trends
- **Efficiency Trends**: Performance over time
- **Environmental Impact**: CO2 emissions and offset calculations
- **Vehicle Comparison**: Multi-vehicle efficiency comparison

### Visualization Support
- Daily/monthly consumption charts
- Driving type distribution
- Cost analysis graphs
- Performance trend lines
- Efficiency comparisons

## 🧪 Testing

### Run Tests
```bash
# Install testing dependencies
pip install pytest pytest-flask

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/
```

### Test Categories
- **Unit Tests**: Individual component testing
- **Integration Tests**: API endpoint testing
- **ML Model Tests**: Prediction accuracy validation
- **Database Tests**: Model and query testing

## 🚀 Deployment

### Production Configuration
1. Set `FLASK_ENV=production`
2. Use production database URL
3. Configure secure secret keys
4. Set up SSL/HTTPS
5. Configure reverse proxy (nginx)
6. Set up monitoring and logging

### Docker Deployment (Optional)
```dockerfile
# Dockerfile example
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

## 🛠 Development

### Project Structure
```
backend/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Dependencies
├── models/              # Database models
├── routes/              # API route blueprints
├── ml_models/           # ML model and handlers
├── ai_integration/      # AI recommendation system
├── utils/               # Utility functions
├── migrations/          # Database migrations
└── tests/               # Test suite
```

### Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact the development team
- Check the documentation and examples

## 🔮 Roadmap

### Phase 1 (Current)
- ✅ Backend API implementation
- ✅ ML model integration
- ✅ Database schema
- ✅ Authentication system

### Phase 2 (Next)
- 🔄 React frontend implementation
- 🔄 Advanced visualizations
- 🔄 Mobile responsive design
- 🔄 Real-time notifications

### Phase 3 (Future)
- 📱 Mobile app (React Native)
- 🌐 Multi-language support
- 📊 Advanced ML models
- 🔗 Third-party integrations