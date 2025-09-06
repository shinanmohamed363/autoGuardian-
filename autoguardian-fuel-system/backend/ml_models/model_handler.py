"""
AutoGuardian Fuel Management System - ML Model Handler
"""

import os
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
import logging
from typing import Dict, List, Tuple, Optional

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FuelConsumptionPredictor:
    """ML Model handler for fuel consumption predictions"""
    
    def __init__(self, model_path: str = None):
        """Initialize the predictor with model path"""
        if model_path is None:
            model_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 
                'best_fuel_model_random_forest.pkl'
            )
        
        self.model_path = model_path
        self.model = None
        self.is_loaded = False
        self.load_model()
    
    def load_model(self) -> bool:
        """Load the trained ML model"""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                self.is_loaded = True
                logger.info(f"✅ ML Model loaded successfully from {self.model_path}")
                logger.info(f"📊 Model type: {type(self.model)}")
                
                # Log model pipeline steps if available
                if hasattr(self.model, 'named_steps'):
                    steps = list(self.model.named_steps.keys())
                    logger.info(f"🔧 Pipeline steps: {steps}")
                
                return True
            else:
                logger.error(f"❌ Model file not found: {self.model_path}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error loading model: {str(e)}")
            self.is_loaded = False
            return False
    
    def preprocess_features(self, vehicle_data: Dict) -> Dict:
        """Preprocess vehicle data for model prediction"""
        try:
            # Map input features to model format
            processed_features = {
                'MAKE': str(vehicle_data.get('make', '')).upper(),
                'MODEL': str(vehicle_data.get('model', '')).upper(),
                'VEHICLE CLASS': str(vehicle_data.get('vehicle_class', '')),
                'ENGINE SIZE': float(self._extract_engine_size(vehicle_data.get('engine_size'))),
                'CYLINDERS': int(vehicle_data.get('cylinders', 4)),
                'TRANSMISSION': self._map_transmission(vehicle_data.get('transmission', '')),
                'FUEL': self._map_fuel_type(vehicle_data.get('fuel_type', ''))
            }
            
            logger.info(f"🔄 Preprocessed features: {processed_features}")
            return processed_features
            
        except Exception as e:
            logger.error(f"❌ Error preprocessing features: {str(e)}")
            raise ValueError(f"Feature preprocessing failed: {str(e)}")
    
    def _extract_engine_size(self, engine_size) -> float:
        """Extract numeric engine size from string"""
        if isinstance(engine_size, (int, float)):
            return float(engine_size)
        
        if isinstance(engine_size, str):
            # Remove 'L' and other characters, extract number
            import re
            numbers = re.findall(r'\d+\.?\d*', engine_size)
            if numbers:
                return float(numbers[0])
        
        return 2.0  # Default fallback
    
    def _map_transmission(self, transmission_type: str) -> str:
        """Map transmission types to model format"""
        transmission_mapping = {
            # Common mappings
            'automatic': 'A4',
            'manual': 'M6',
            'cvt': 'AV',
            'semi-automatic': 'AS',
            'semi_automatic': 'AS',
            
            # Direct mappings (already in correct format)
            'a4': 'A4', 'a5': 'A5', 'a6': 'A6', 'a7': 'A7', 'a8': 'A8', 
            'a9': 'A9', 'a10': 'A10',
            'm5': 'M5', 'm6': 'M6', 'm7': 'M7',
            'av': 'AV', 'as': 'AS',
            
            # Extended mappings
            'auto': 'A4',
            'stick': 'M6',
            'manual_6_speed': 'M6',
            'automatic_8_speed': 'A8',
            'continuously_variable': 'AV'
        }
        
        transmission_clean = str(transmission_type).lower().strip()
        return transmission_mapping.get(transmission_clean, 'A4')  # Default to A4
    
    def _map_fuel_type(self, fuel_type: str) -> str:
        """Map fuel types to model format"""
        fuel_mapping = {
            # Gasoline types
            'regular_gasoline': 'X',
            'regular gasoline': 'X',
            'regular': 'X',
            'gasoline': 'X',
            'gas': 'X',
            'petrol': 'X',
            'unleaded': 'X',
            
            # Premium gasoline
            'premium_gasoline': 'Z',
            'premium gasoline': 'Z',
            'premium': 'Z',
            'premium_unleaded': 'Z',
            'high_octane': 'Z',
            'super': 'Z',
            
            # Diesel
            'diesel': 'D',
            'biodiesel': 'D',
            
            # Hybrid (map to regular gasoline)
            'hybrid': 'X',
            'hybrid_gasoline': 'X',
            
            # Electric (special case)
            'electric': 'E',
            'ev': 'E',
            
            # Direct mappings
            'x': 'X', 'z': 'Z', 'd': 'D', 'e': 'E'
        }
        
        fuel_clean = str(fuel_type).lower().strip()
        return fuel_mapping.get(fuel_clean, 'X')  # Default to regular gasoline
    
    def predict(self, vehicle_data: Dict) -> Dict:
        """Make fuel consumption predictions"""
        if not self.is_loaded:
            raise RuntimeError("Model is not loaded. Cannot make predictions.")
        
        try:
            # Preprocess features
            features = self.preprocess_features(vehicle_data)
            
            # Create DataFrame for model input
            input_df = pd.DataFrame([features])
            logger.info(f"📊 Model input shape: {input_df.shape}")
            logger.info(f"📊 Model input columns: {list(input_df.columns)}")
            
            # Make prediction
            predictions = self.model.predict(input_df)
            logger.info(f"🔮 Raw predictions shape: {predictions.shape}")
            logger.info(f"🔮 Raw predictions: {predictions}")
            
            # Extract predictions (handle different output formats)
            if len(predictions.shape) > 1 and predictions.shape[1] >= 3:
                # Multi-output format [combined, highway, emissions]
                combined_consumption = float(predictions[0][0])
                highway_consumption = float(predictions[0][1])
                emissions = float(predictions[0][2])
            elif len(predictions.shape) > 1 and predictions.shape[1] >= 2:
                # Two-output format [combined, emissions]
                combined_consumption = float(predictions[0][0])
                highway_consumption = combined_consumption * 0.85  # Estimate
                emissions = float(predictions[0][1])
            else:
                # Single output (combined consumption only)
                combined_consumption = float(predictions[0])
                highway_consumption = combined_consumption * 0.85
                emissions = self._estimate_emissions(combined_consumption)
            
            # Calculate additional metrics
            city_consumption = combined_consumption * 1.20  # 20% worse in city
            efficiency_rating = self._get_efficiency_rating(combined_consumption)
            
            # Calculate projections
            annual_fuel_cost, annual_co2_emissions, mpg_equivalent = self._calculate_projections(
                combined_consumption, emissions
            )
            
            result = {
                'combined_l_100km': round(combined_consumption, 2),
                'highway_l_100km': round(highway_consumption, 2),
                'city_l_100km': round(city_consumption, 2),
                'emissions_g_km': round(emissions, 2),
                'efficiency_rating': efficiency_rating,
                'efficiency_stars': self._get_efficiency_stars(combined_consumption),
                'annual_fuel_cost': round(annual_fuel_cost, 2),
                'annual_co2_emissions': round(annual_co2_emissions, 2),
                'mpg_equivalent': round(mpg_equivalent, 1),
                'prediction_metadata': {
                    'model_used': 'random_forest',
                    'prediction_date': datetime.utcnow().isoformat(),
                    'features_used': list(features.keys()),
                    'preprocessing_applied': True
                }
            }
            
            logger.info(f"✅ Prediction successful: {result}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Prediction error: {str(e)}")
            raise RuntimeError(f"Prediction failed: {str(e)}")
    
    def _estimate_emissions(self, consumption: float) -> float:
        """Estimate CO2 emissions based on consumption"""
        # Rough estimation: consumption * 23.1 (approximate CO2 factor for gasoline)
        return consumption * 23.1
    
    def _get_efficiency_rating(self, consumption: float) -> str:
        """Get efficiency rating with stars"""
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
    
    def _get_efficiency_stars(self, consumption: float) -> int:
        """Get efficiency rating as number of stars (1-5)"""
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
    
    def _calculate_projections(self, consumption: float, emissions: float) -> Tuple[float, float, float]:
        """Calculate annual projections and MPG equivalent"""
        # Annual projections (15,000 km/year)
        annual_km = 15000
        fuel_price = 1.50  # CAD per liter
        
        annual_liters = (consumption * annual_km) / 100
        annual_fuel_cost = annual_liters * fuel_price
        annual_co2_emissions = (emissions * annual_km) / 1000  # Convert g to kg
        
        # MPG equivalent conversion
        mpg_equivalent = 235.214583 / consumption  # L/100km to MPG conversion
        
        return annual_fuel_cost, annual_co2_emissions, mpg_equivalent
    
    def predict_multiple(self, vehicles_data: List[Dict]) -> List[Dict]:
        """Make predictions for multiple vehicles"""
        results = []
        for vehicle_data in vehicles_data:
            try:
                prediction = self.predict(vehicle_data)
                prediction['vehicle_id'] = vehicle_data.get('vehicle_id', 'unknown')
                results.append(prediction)
            except Exception as e:
                logger.error(f"❌ Failed to predict for vehicle {vehicle_data.get('vehicle_id')}: {str(e)}")
                results.append({
                    'vehicle_id': vehicle_data.get('vehicle_id', 'unknown'),
                    'error': str(e),
                    'success': False
                })
        return results
    
    def get_model_info(self) -> Dict:
        """Get information about the loaded model"""
        if not self.is_loaded:
            return {'error': 'Model not loaded'}
        
        info = {
            'model_path': self.model_path,
            'model_type': str(type(self.model)),
            'is_loaded': self.is_loaded,
            'last_loaded': datetime.utcnow().isoformat()
        }
        
        try:
            if hasattr(self.model, 'named_steps'):
                info['pipeline_steps'] = list(self.model.named_steps.keys())
                
                # Get feature information from preprocessor
                if 'preprocessor' in self.model.named_steps:
                    preprocessor = self.model.named_steps['preprocessor']
                    if hasattr(preprocessor, 'transformers'):
                        info['feature_transformers'] = [
                            {'name': name, 'columns': cols} 
                            for name, transformer, cols in preprocessor.transformers
                        ]
            
            # Try to get feature importance if available
            if hasattr(self.model, 'feature_importances_'):
                info['has_feature_importance'] = True
            elif hasattr(self.model, 'named_steps') and 'model' in self.model.named_steps:
                model_step = self.model.named_steps['model']
                if hasattr(model_step, 'estimators_'):
                    info['has_feature_importance'] = True
                    info['model_estimators'] = len(model_step.estimators_)
        
        except Exception as e:
            info['model_info_error'] = str(e)
        
        return info
    
    def validate_input(self, vehicle_data: Dict) -> Tuple[bool, List[str]]:
        """Validate input data for prediction"""
        errors = []
        required_fields = ['make', 'model', 'vehicle_class', 'engine_size', 'cylinders', 'transmission', 'fuel_type']
        
        for field in required_fields:
            if field not in vehicle_data:
                errors.append(f"Missing required field: {field}")
            elif vehicle_data[field] is None or vehicle_data[field] == '':
                errors.append(f"Empty value for required field: {field}")
        
        # Validate specific field types and ranges
        if 'cylinders' in vehicle_data:
            try:
                cylinders = int(vehicle_data['cylinders'])
                if cylinders < 1 or cylinders > 12:
                    errors.append("Cylinders must be between 1 and 12")
            except (ValueError, TypeError):
                errors.append("Cylinders must be a valid integer")
        
        if 'engine_size' in vehicle_data:
            try:
                engine_size = self._extract_engine_size(vehicle_data['engine_size'])
                if engine_size < 0.5 or engine_size > 8.0:
                    errors.append("Engine size must be between 0.5L and 8.0L")
            except (ValueError, TypeError):
                errors.append("Engine size must be a valid number")
        
        return len(errors) == 0, errors

# Global model instance
_predictor_instance = None

def get_predictor() -> FuelConsumptionPredictor:
    """Get global predictor instance (singleton pattern)"""
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = FuelConsumptionPredictor()
    return _predictor_instance

def predict_fuel_consumption(vehicle_data: Dict) -> Dict:
    """Convenience function for making predictions"""
    predictor = get_predictor()
    return predictor.predict(vehicle_data)

def validate_vehicle_data(vehicle_data: Dict) -> Tuple[bool, List[str]]:
    """Convenience function for validating vehicle data"""
    predictor = get_predictor()
    return predictor.validate_input(vehicle_data)