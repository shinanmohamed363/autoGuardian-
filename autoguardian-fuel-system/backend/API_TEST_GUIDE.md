# AutoGuardian AI Recommendations API Test Guide

## Complete Postman Testing Sequence

### Base URL
```
http://127.0.0.1:5000
```

## Step 1: User Registration & Authentication

### 1.1 Register New User
**Method:** POST  
**URL:** `/api/auth/register`  
**Headers:**
```json
{
  "Content-Type": "application/json"
}
```
**Body (JSON):**
```json
{
  "username": "testuser2024",
  "email": "testuser2024@example.com", 
  "password": "Password123!"
}
```

### 1.2 Login to Get JWT Token
**Method:** POST  
**URL:** `/api/auth/login`  
**Headers:**
```json
{
  "Content-Type": "application/json"
}
```
**Body (JSON):**
```json
{
  "username": "testuser2024",
  "password": "Password123!"
}
```
**Response:** Save the `access_token` from response for subsequent requests.

## Step 2: Vehicle Registration

### 2.1 Register Vehicle
**Method:** POST  
**URL:** `/api/vehicles`  
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"
}
```
**Body (JSON):**
```json
{
  "vehicle_id": "HONDA2021TEST",
  "vehicle_name": "My Honda Civic",
  "make": "Honda",
  "model": "Civic",
  "year": 2021,
  "vehicle_class": "Compact",
  "engine_size": 2.0,
  "cylinders": 4,
  "transmission": "Automatic",
  "fuel_type": "Regular Gasoline",
  "tank_capacity": 47.0,
  "full_tank_capacity": 47.0,
  "starting_odometer_value": 15000,
  "initial_tank_percentage": 90.0
}
```

## Step 3: Add Fuel Records (Multiple Records for Better AI Analysis)

### 3.1 First Fuel Record
**Method:** POST  
**URL:** `/api/fuel-records`  
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"
}
```
**Body (JSON):**
```json
{
  "vehicle_id": "HONDA2021TEST",
  "fuel_added": 32.5,
  "fuel_price": 1.45,
  "odo_meter_current_value": 15380,
  "existing_tank_percentage": 20.0,
  "after_refuel_percentage": 95.0,
  "fuel_type": "Regular Gasoline",
  "record_date": "2025-08-25",
  "record_time": "14:30",
  "driving_type": "mix",
  "location": "Petro Canada",
  "notes": "First refuel - mostly city driving"
}
```

### 3.2 Second Fuel Record  
**Method:** POST  
**URL:** `/api/fuel-records`  
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"
}
```
**Body (JSON):**
```json
{
  "vehicle_id": "HONDA2021TEST",
  "fuel_added": 28.8,
  "fuel_price": 1.52,
  "odo_meter_current_value": 15720,
  "existing_tank_percentage": 25.0,
  "after_refuel_percentage": 90.0,
  "fuel_type": "Regular Gasoline",
  "record_date": "2025-08-30",
  "record_time": "09:15",
  "driving_type": "highway",
  "location": "Shell",
  "notes": "Highway trip - better efficiency expected"
}
```

### 3.3 Third Fuel Record (Higher Consumption)
**Method:** POST  
**URL:** `/api/fuel-records`  
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"
}
```
**Body (JSON):**
```json
{
  "vehicle_id": "HONDA2021TEST",
  "fuel_added": 38.2,
  "fuel_price": 1.48,
  "odo_meter_current_value": 16050,
  "existing_tank_percentage": 15.0,
  "after_refuel_percentage": 98.0,
  "fuel_type": "Regular Gasoline",
  "record_date": "2025-09-01",
  "record_time": "16:45",
  "driving_type": "city",
  "location": "Esso",
  "notes": "Heavy city traffic - poor fuel economy"
}
```

## Step 4: Generate ML Predictions

### 4.1 Generate ML Prediction
**Method:** POST  
**URL:** `/api/predictions`  
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"
}
```
**Body (JSON):**
```json
{
  "vehicle_id": 3
}
```

### 4.2 View Vehicle with ML Data
**Method:** GET  
**URL:** `/api/vehicles/3`  
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"
}
```

## Step 5: AI Recommendation Generation & Testing

### 5.1 Test AI Connection
**Method:** GET  
**URL:** `/api/recommendations/test-genai`  
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"
}
```
**Expected Response:**
```json
{
  "genai_test": {
    "status": "success",
    "message": "GenAI connection successful"
  },
  "api_configured": true
}
```

### 5.2 Generate Efficiency Recommendation
**Method:** POST  
**URL:** `/api/recommendations/generate`  
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"
}
```
**Body (JSON):**
```json
{
  "vehicle_id": 3,
  "recommendation_type": "efficiency"
}
```

### 5.3 Generate Maintenance Recommendation
**Method:** POST  
**URL:** `/api/recommendations/generate`  
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"
}
```
**Body (JSON):**
```json
{
  "vehicle_id": 3,
  "recommendation_type": "maintenance"
}
```

## Step 6: View & Manage Recommendations

### 6.1 Get All User Recommendations
**Method:** GET  
**URL:** `/api/recommendations/7` (Replace 7 with your actual user ID)
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"
}
```
**Query Parameters (Optional):**
- `limit=10` - Limit number of results
- `unread_only=true` - Only unread recommendations  
- `priority=high` - Filter by priority (low, medium, high, critical)

### 6.2 Get Vehicle-Specific Recommendations
**Method:** GET  
**URL:** `/api/recommendations/vehicle/3`  
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"
}
```

### 6.3 Get Specific Recommendation Details
**Method:** GET  
**URL:** `/api/recommendations/1` (Replace 1 with actual recommendation ID)
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"
}
```

### 6.4 Get Recommendations Summary
**Method:** GET  
**URL:** `/api/recommendations/summary`  
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"
}
```

### 6.5 Mark Recommendation as Read
**Method:** PUT  
**URL:** `/api/recommendations/1/read` (Replace 1 with actual recommendation ID)
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"
}
```

### 6.6 Mark Recommendation as Implemented
**Method:** PUT  
**URL:** `/api/recommendations/1/implement` (Replace 1 with actual recommendation ID)
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"
}
```
**Body (JSON - Optional):**
```json
{
  "implementation_notes": "Replaced air filter and checked tire pressure as recommended"
}
```

## Step 7: Analytics & Statistics

### 7.1 Get Vehicle Analytics Dashboard
**Method:** GET  
**URL:** `/api/analytics/dashboard/7` (Replace 7 with your user ID)
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"
}
```

### 7.2 Get Comprehensive Vehicle Report
**Method:** POST  
**URL:** `/api/analytics/comprehensive-report/3`  
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"
}
```
**Body (JSON):**
```json
{
  "start_date": "2025-08-01",
  "end_date": "2025-09-01"
}
```

### 7.3 Get Driving Patterns Analysis
**Method:** GET  
**URL:** `/api/analytics/driving-patterns/3`  
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"
}
```

### 7.4 Get Consumption Trends
**Method:** GET  
**URL:** `/api/analytics/consumption-trends/3`  
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"
}
```

### 7.5 Get Fuel Records with Analytics
**Method:** GET  
**URL:** `/api/fuel-records/3`  
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_JWT_TOKEN_HERE"
}
```
**Query Parameters (Optional):**
- `limit=10` - Limit number of records
- `days=30` - Only records from last N days

## Sample Expected AI Response Structure

### Efficiency Recommendation Response:
```json
{
  "message": "1 recommendations generated successfully",
  "recommendations": [
    {
      "id": 1,
      "recommendation_type": "efficiency",
      "recommendation_title": "Personalized Fuel Efficiency Guide",
      "priority_level": "medium",
      "category": "fuel_efficiency",
      "impact_score": 7.5,
      "confidence_level": 0.82,
      "ai_model_used": "gemini-2.0-flash",
      "performance_analysis": "Vehicle consuming X.XX L/100km vs predicted Y.YY L/100km",
      "recommendation_text": "## Detailed AI-generated efficiency recommendations..."
    }
  ]
}
```

### Maintenance Recommendation Response:
```json
{
  "message": "1 recommendations generated successfully", 
  "recommendations": [
    {
      "id": 2,
      "recommendation_type": "maintenance",
      "recommendation_title": "AI-Powered Maintenance Analysis",
      "priority_level": "high",
      "category": "maintenance", 
      "impact_score": 8.0,
      "confidence_level": 0.85,
      "ai_model_used": "gemini-2.0-flash",
      "performance_analysis": "Analysis of vehicle maintenance needs...",
      "recommendation_text": "## Detailed AI-generated maintenance recommendations..."
    }
  ]
}
```

## Key Features to Test:

1. **Real Data Integration**: AI uses actual fuel consumption from your fuel records
2. **ML Model Predictions**: Compares actual vs predicted efficiency 
3. **Contextual Recommendations**: AI considers vehicle specs, driving patterns, and performance
4. **Priority Assignment**: Automatic priority based on consumption deviation
5. **Comprehensive Analysis**: Detailed recommendations with cost savings estimates
6. **Status Management**: Track read/unread and implementation status

## Notes:
- Replace `YOUR_JWT_TOKEN_HERE` with the actual token from login response
- Replace `{USER_ID}` with your actual user ID from registration
- Replace `{RECOMMENDATION_ID}` with actual recommendation IDs from responses
- Server must be running on `http://127.0.0.1:5000`

The AI will generate personalized recommendations based on your actual vehicle data, fuel records, and ML predictions!