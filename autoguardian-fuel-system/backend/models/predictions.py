"""
AutoGuardian Fuel Management System - ML Prediction Models
"""

from database import db
from datetime import datetime

class MLPrediction(db.Model):
    """ML prediction model for storing machine learning predictions"""
    
    __tablename__ = 'ml_predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    
    # Prediction results
    combined_l_100km = db.Column(db.Numeric(6, 2))
    highway_l_100km = db.Column(db.Numeric(6, 2))
    city_l_100km = db.Column(db.Numeric(6, 2))
    emissions_g_km = db.Column(db.Numeric(8, 2))
    efficiency_rating = db.Column(db.String(50))
    
    # Model metadata
    model_version = db.Column(db.String(20), default='1.0')
    confidence_score = db.Column(db.Numeric(3, 2))  # 0.00 to 1.00
    prediction_source = db.Column(db.String(50), default='random_forest')
    
    # Additional predictions
    annual_fuel_cost = db.Column(db.Numeric(8, 2))
    annual_co2_emissions = db.Column(db.Numeric(10, 2))
    mpg_equivalent = db.Column(db.Numeric(5, 1))
    
    # Timestamps
    prediction_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, vehicle_id, combined_l_100km, highway_l_100km=None, city_l_100km=None,
                 emissions_g_km=None, efficiency_rating=None, confidence_score=None,
                 model_version='1.0', prediction_source='random_forest'):
        """Initialize ML prediction"""
        self.vehicle_id = vehicle_id
        self.combined_l_100km = combined_l_100km
        self.highway_l_100km = highway_l_100km or combined_l_100km * 0.85
        self.city_l_100km = city_l_100km or combined_l_100km * 1.20
        self.emissions_g_km = emissions_g_km
        self.efficiency_rating = efficiency_rating or self._calculate_efficiency_rating(combined_l_100km)
        self.confidence_score = confidence_score
        self.model_version = model_version
        self.prediction_source = prediction_source
        
        # Calculate additional metrics (commented out due to missing DB columns)
        # self._calculate_additional_metrics()
    
    def _calculate_efficiency_rating(self, consumption):
        """Calculate efficiency rating based on consumption"""
        consumption = float(consumption)
        if consumption < 6:
            return "⭐⭐⭐⭐⭐ Excellent"
        elif consumption < 8:
            return "⭐⭐⭐⭐ Good"
        elif consumption < 10:
            return "⭐⭐⭐ Average"
        elif consumption < 12:
            return "⭐⭐ Below Average"
        else:
            return "⭐ Poor"
    
    def _calculate_additional_metrics(self):
        """Calculate additional prediction metrics"""
        if self.combined_l_100km:
            # Annual cost estimation (15,000 km/year, $1.50/L)
            annual_km = 15000
            fuel_price = 1.50
            annual_liters = (float(self.combined_l_100km) * annual_km) / 100
            self.annual_fuel_cost = annual_liters * fuel_price
            
            # MPG equivalent conversion
            self.mpg_equivalent = 235.214583 / float(self.combined_l_100km)
        
        if self.emissions_g_km:
            # Annual CO2 emissions (kg)
            annual_km = 15000
            self.annual_co2_emissions = (float(self.emissions_g_km) * annual_km) / 1000
    
    @property
    def efficiency_stars(self):
        """Get number of efficiency stars (1-5)"""
        if not self.combined_l_100km:
            return 0
        
        consumption = float(self.combined_l_100km)
        if consumption < 6:
            return 5
        elif consumption < 8:
            return 4
        elif consumption < 10:
            return 3
        elif consumption < 12:
            return 2
        else:
            return 1
    
    @property
    def environmental_impact(self):
        """Get environmental impact information"""
        if not self.annual_co2_emissions:
            return None
        
        annual_co2 = float(self.annual_co2_emissions)
        trees_needed = annual_co2 / 22  # One tree absorbs ~22kg CO2 per year
        
        return {
            'annual_co2_kg': annual_co2,
            'trees_to_offset': round(trees_needed),
            'impact_level': self._get_impact_level(annual_co2)
        }
    
    def _get_impact_level(self, annual_co2):
        """Determine environmental impact level"""
        if annual_co2 < 2000:
            return 'Low'
        elif annual_co2 < 3500:
            return 'Moderate'
        elif annual_co2 < 5000:
            return 'High'
        else:
            return 'Very High'
    
    def compare_with_actual(self, actual_consumption):
        """Compare prediction with actual consumption"""
        if not self.combined_l_100km or not actual_consumption:
            return None
        
        predicted = float(self.combined_l_100km)
        actual = float(actual_consumption)
        
        difference = actual - predicted
        percentage_diff = (difference / predicted) * 100
        
        if percentage_diff < -10:
            performance = "Much Better Than Expected"
            status = "excellent"
        elif percentage_diff < 0:
            performance = "Better Than Expected"
            status = "good"
        elif percentage_diff < 10:
            performance = "Close to Expected"
            status = "average"
        else:
            performance = "Worse Than Expected"
            status = "poor"
        
        return {
            'predicted_consumption': predicted,
            'actual_consumption': actual,
            'difference_l_100km': round(difference, 2),
            'percentage_difference': round(percentage_diff, 1),
            'performance': performance,
            'status': status
        }
    
    def to_dict(self, include_analysis=False):
        """Convert prediction to dictionary"""
        data = {
            'id': self.id,
            'vehicle_id': self.vehicle_id,
            'combined_l_100km': float(self.combined_l_100km) if self.combined_l_100km else None,
            'highway_l_100km': float(self.highway_l_100km) if self.highway_l_100km else None,
            'city_l_100km': float(self.city_l_100km) if self.city_l_100km else None,
            'emissions_g_km': float(self.emissions_g_km) if self.emissions_g_km else None,
            'efficiency_rating': self.efficiency_rating,
            'efficiency_stars': self.efficiency_stars,
            'confidence_score': float(self.confidence_score) if self.confidence_score else None,
            'model_version': self.model_version,
            'prediction_source': self.prediction_source,
            'annual_fuel_cost': float(self.annual_fuel_cost) if self.annual_fuel_cost else None,
            'annual_co2_emissions': float(self.annual_co2_emissions) if self.annual_co2_emissions else None,
            'mpg_equivalent': float(self.mpg_equivalent) if self.mpg_equivalent else None,
            'environmental_impact': self.environmental_impact,
            'prediction_date': self.prediction_date.isoformat(),
            'created_at': self.created_at.isoformat()
        }
        
        if include_analysis:
            # Add comparison with actual data if available
            from .fuel_record import FuelRecord
            recent_records = FuelRecord.get_vehicle_records(self.vehicle_id, limit=5)
            if recent_records:
                actual_avg = sum(r.actual_consumption_l_100km for r in recent_records) / len(recent_records)
                data['actual_comparison'] = self.compare_with_actual(actual_avg)
        
        return data
    
    @classmethod
    def get_latest_prediction(cls, vehicle_id):
        """Get latest prediction for a vehicle"""
        return cls.query.filter_by(vehicle_id=vehicle_id).order_by(
            db.desc(cls.prediction_date)
        ).first()
    
    @classmethod
    def get_prediction_history(cls, vehicle_id, limit=10):
        """Get prediction history for a vehicle"""
        return cls.query.filter_by(vehicle_id=vehicle_id).order_by(
            db.desc(cls.prediction_date)
        ).limit(limit).all()
    
    @classmethod
    def create_from_model_output(cls, vehicle_id, model_output, confidence_score=None):
        """Create prediction from ML model output"""
        # Assuming model_output is a numpy array [combined, highway, emissions]
        combined_consumption = float(model_output[0])
        highway_consumption = float(model_output[1]) if len(model_output) > 1 else combined_consumption * 0.85
        emissions = float(model_output[2]) if len(model_output) > 2 else None
        
        return cls(
            vehicle_id=vehicle_id,
            combined_l_100km=combined_consumption,
            highway_l_100km=highway_consumption,
            city_l_100km=combined_consumption * 1.20,
            emissions_g_km=emissions,
            confidence_score=confidence_score
        )
    
    def is_outdated(self, days=30):
        """Check if prediction is outdated"""
        from datetime import timedelta
        return (datetime.utcnow() - self.prediction_date) > timedelta(days=days)
    
    def __repr__(self):
        return f'<MLPrediction {self.id}: {self.vehicle_id} - {self.combined_l_100km}L/100km>'