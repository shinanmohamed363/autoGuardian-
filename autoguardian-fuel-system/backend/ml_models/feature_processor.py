"""
AutoGuardian Fuel Management System - Feature Processing Utilities
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
import re
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

class FeatureProcessor:
    """Handle feature processing and data transformations"""
    
    def __init__(self):
        """Initialize feature processor"""
        self.vehicle_class_mapping = self._create_vehicle_class_mapping()
        self.make_standardization = self._create_make_standardization()
        self.model_standardization = self._create_model_standardization()
    
    def _create_vehicle_class_mapping(self) -> Dict[str, str]:
        """Create mapping for vehicle class standardization"""
        return {
            # Compact vehicles
            'compact': 'COMPACT',
            'subcompact': 'SUBCOMPACT',
            'sedan': 'COMPACT',
            'small_car': 'COMPACT',
            
            # Mid-size vehicles
            'midsize': 'MID-SIZE',
            'mid-size': 'MID-SIZE',
            'mid_size': 'MID-SIZE',
            'medium': 'MID-SIZE',
            
            # Full-size vehicles
            'full-size': 'FULL-SIZE',
            'full_size': 'FULL-SIZE',
            'fullsize': 'FULL-SIZE',
            'large': 'FULL-SIZE',
            
            # SUV categories
            'suv': 'SUV: SMALL',
            'small_suv': 'SUV: SMALL',
            'compact_suv': 'SUV: SMALL',
            'midsize_suv': 'SUV: STANDARD',
            'mid-size_suv': 'SUV: STANDARD',
            'large_suv': 'SUV: STANDARD',
            'full-size_suv': 'SUV: STANDARD',
            
            # Pickup trucks
            'pickup': 'PICKUP TRUCK: STANDARD',
            'truck': 'PICKUP TRUCK: STANDARD',
            'pickup_truck': 'PICKUP TRUCK: STANDARD',
            'small_pickup': 'PICKUP TRUCK: SMALL',
            'compact_pickup': 'PICKUP TRUCK: SMALL',
            
            # Station wagons
            'wagon': 'STATION WAGON: SMALL',
            'station_wagon': 'STATION WAGON: SMALL',
            'estate': 'STATION WAGON: SMALL',
            
            # Vans
            'van': 'VAN: CARGO',
            'minivan': 'VAN: PASSENGER',
            'cargo_van': 'VAN: CARGO',
            'passenger_van': 'VAN: PASSENGER',
            
            # Sports cars
            'sports': 'TWO-SEATER',
            'sports_car': 'TWO-SEATER',
            'coupe': 'TWO-SEATER',
            'convertible': 'TWO-SEATER',
            
            # Specialty vehicles
            'motorcycle': 'SPECIAL PURPOSE VEHICLE',
            'specialty': 'SPECIAL PURPOSE VEHICLE'
        }
    
    def _create_make_standardization(self) -> Dict[str, str]:
        """Create standardization mapping for vehicle makes"""
        return {
            # Common standardizations
            'bmw': 'BMW',
            'volkswagen': 'VOLKSWAGEN',
            'vw': 'VOLKSWAGEN',
            'mercedes': 'MERCEDES-BENZ',
            'mercedes-benz': 'MERCEDES-BENZ',
            'mb': 'MERCEDES-BENZ',
            'gm': 'GENERAL MOTORS',
            'general motors': 'GENERAL MOTORS',
            'ford motor company': 'FORD',
            'toyota motor corporation': 'TOYOTA',
            'honda motor co.': 'HONDA',
            'nissan motor co.': 'NISSAN',
            'hyundai motor company': 'HYUNDAI',
            'kia motors': 'KIA',
            'mitsubishi motors': 'MITSUBISHI',
            'subaru corporation': 'SUBARU',
            'mazda motor corporation': 'MAZDA',
            'audi ag': 'AUDI',
            'porsche ag': 'PORSCHE',
            'jaguar land rover': 'JAGUAR',
            'land rover': 'LAND ROVER',
            'volvo cars': 'VOLVO',
            'tesla inc.': 'TESLA',
            'fiat chrysler': 'CHRYSLER',
            'stellantis': 'CHRYSLER'
        }
    
    def _create_model_standardization(self) -> Dict[str, str]:
        """Create standardization mapping for common model names"""
        return {
            # Common model name standardizations
            'camry hybrid': 'CAMRY',
            'accord hybrid': 'ACCORD',
            'civic hatchback': 'CIVIC',
            'corolla hybrid': 'COROLLA',
            'prius prime': 'PRIUS',
            'model s': 'MODEL S',
            'model 3': 'MODEL 3',
            'model x': 'MODEL X',
            'model y': 'MODEL Y',
            'f-150': 'F-150',
            'f150': 'F-150',
            'silverado': 'SILVERADO',
            'sierra': 'SIERRA',
            'ram 1500': 'RAM',
            'cherokee': 'CHEROKEE',
            'wrangler': 'WRANGLER'
        }
    
    def standardize_make(self, make: str) -> str:
        """Standardize vehicle make"""
        if not make:
            return 'UNKNOWN'
        
        make_clean = str(make).strip().lower()
        return self.make_standardization.get(make_clean, make.upper())
    
    def standardize_model(self, model: str) -> str:
        """Standardize vehicle model"""
        if not model:
            return 'UNKNOWN'
        
        model_clean = str(model).strip().lower()
        return self.model_standardization.get(model_clean, model.upper())
    
    def standardize_vehicle_class(self, vehicle_class: str) -> str:
        """Standardize vehicle class"""
        if not vehicle_class:
            return 'COMPACT'  # Default
        
        class_clean = str(vehicle_class).strip().lower()
        return self.vehicle_class_mapping.get(class_clean, vehicle_class.upper())
    
    def extract_numeric_engine_size(self, engine_size: Any) -> float:
        """Extract numeric engine size from various formats"""
        if isinstance(engine_size, (int, float)):
            return max(0.5, min(8.0, float(engine_size)))  # Clamp between 0.5 and 8.0
        
        if isinstance(engine_size, str):
            # Remove common suffixes and extract number
            engine_str = engine_size.lower().strip()
            engine_str = engine_str.replace('l', '').replace('liter', '').replace('litre', '')
            engine_str = engine_str.replace('cc', '').replace('v', '').strip()
            
            # Extract numeric values
            numbers = re.findall(r'\d+\.?\d*', engine_str)
            if numbers:
                size = float(numbers[0])
                
                # Handle CC to L conversion
                if 'cc' in engine_size.lower() and size > 50:
                    size = size / 1000  # Convert CC to L
                
                return max(0.5, min(8.0, size))  # Clamp between 0.5 and 8.0
        
        return 2.0  # Default fallback
    
    def validate_cylinders(self, cylinders: Any) -> int:
        """Validate and standardize cylinder count"""
        try:
            cyl_count = int(cylinders)
            return max(1, min(12, cyl_count))  # Clamp between 1 and 12
        except (ValueError, TypeError):
            return 4  # Default fallback
    
    def standardize_transmission(self, transmission: str) -> str:
        """Standardize transmission type"""
        if not transmission:
            return 'A4'  # Default automatic
        
        trans_clean = str(transmission).strip().lower()
        
        # Direct mappings (already in correct format)
        direct_mappings = ['a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10', 
                          'm5', 'm6', 'm7', 'av', 'as']
        if trans_clean in direct_mappings:
            return trans_clean.upper()
        
        # Pattern-based mappings
        if any(pattern in trans_clean for pattern in ['cvt', 'continuously', 'variable']):
            return 'AV'
        
        if any(pattern in trans_clean for pattern in ['manual', 'stick', 'mt']):
            # Try to extract speed
            speed_match = re.search(r'(\d+)', trans_clean)
            if speed_match:
                speed = int(speed_match.group(1))
                return f'M{min(7, max(5, speed))}'  # M5-M7
            return 'M6'  # Default manual
        
        if any(pattern in trans_clean for pattern in ['auto', 'automatic', 'at']):
            # Try to extract speed
            speed_match = re.search(r'(\d+)', trans_clean)
            if speed_match:
                speed = int(speed_match.group(1))
                return f'A{min(10, max(4, speed))}'  # A4-A10
            return 'A6'  # Default automatic
        
        if any(pattern in trans_clean for pattern in ['semi', 'tiptronic', 'paddle']):
            return 'AS'
        
        return 'A6'  # Default fallback
    
    def standardize_fuel_type(self, fuel_type: str) -> str:
        """Standardize fuel type"""
        if not fuel_type:
            return 'X'  # Default regular gasoline
        
        fuel_clean = str(fuel_type).strip().lower()
        
        # Direct mappings
        if fuel_clean in ['x', 'z', 'd', 'e']:
            return fuel_clean.upper()
        
        # Gasoline types
        regular_patterns = ['regular', 'gasoline', 'gas', 'petrol', 'unleaded', '87', 'octane']
        if any(pattern in fuel_clean for pattern in regular_patterns):
            return 'X'
        
        # Premium gasoline
        premium_patterns = ['premium', 'super', 'high', '91', '93', '95', 'plus']
        if any(pattern in fuel_clean for pattern in premium_patterns):
            return 'Z'
        
        # Diesel
        diesel_patterns = ['diesel', 'biodiesel', 'tdi', 'cdi']
        if any(pattern in fuel_clean for pattern in diesel_patterns):
            return 'D'
        
        # Electric
        electric_patterns = ['electric', 'ev', 'battery', 'bev']
        if any(pattern in fuel_clean for pattern in electric_patterns):
            return 'E'
        
        # Hybrid (map to regular gasoline)
        hybrid_patterns = ['hybrid', 'hev', 'phev', 'plug']
        if any(pattern in fuel_clean for pattern in hybrid_patterns):
            return 'X'
        
        return 'X'  # Default fallback
    
    def process_vehicle_features(self, vehicle_data: Dict) -> Dict:
        """Process all vehicle features for ML model input"""
        processed = {}
        
        try:
            # Required features with processing
            processed['MAKE'] = self.standardize_make(vehicle_data.get('make'))
            processed['MODEL'] = self.standardize_model(vehicle_data.get('model'))
            processed['VEHICLE CLASS'] = self.standardize_vehicle_class(vehicle_data.get('vehicle_class'))
            processed['ENGINE SIZE'] = self.extract_numeric_engine_size(vehicle_data.get('engine_size'))
            processed['CYLINDERS'] = self.validate_cylinders(vehicle_data.get('cylinders'))
            processed['TRANSMISSION'] = self.standardize_transmission(vehicle_data.get('transmission'))
            processed['FUEL'] = self.standardize_fuel_type(vehicle_data.get('fuel_type'))
            
            logger.info(f"🔄 Processed features: {processed}")
            return processed
            
        except Exception as e:
            logger.error(f"❌ Feature processing error: {str(e)}")
            raise ValueError(f"Failed to process vehicle features: {str(e)}")
    
    def validate_processed_features(self, features: Dict) -> Tuple[bool, List[str]]:
        """Validate processed features"""
        errors = []
        
        # Check required fields
        required_fields = ['MAKE', 'MODEL', 'VEHICLE CLASS', 'ENGINE SIZE', 
                          'CYLINDERS', 'TRANSMISSION', 'FUEL']
        
        for field in required_fields:
            if field not in features or features[field] is None:
                errors.append(f"Missing processed field: {field}")
        
        # Validate ranges
        if 'ENGINE SIZE' in features:
            engine_size = features['ENGINE SIZE']
            if not (0.5 <= engine_size <= 8.0):
                errors.append(f"Engine size {engine_size} outside valid range (0.5-8.0L)")
        
        if 'CYLINDERS' in features:
            cylinders = features['CYLINDERS']
            if not (1 <= cylinders <= 12):
                errors.append(f"Cylinders {cylinders} outside valid range (1-12)")
        
        # Validate categorical values
        valid_fuel_types = ['X', 'Z', 'D', 'E']
        if 'FUEL' in features and features['FUEL'] not in valid_fuel_types:
            errors.append(f"Invalid fuel type: {features['FUEL']}. Must be one of {valid_fuel_types}")
        
        valid_transmission_pattern = re.compile(r'^(A|M)\d+$|^(AV|AS)$')
        if 'TRANSMISSION' in features:
            if not valid_transmission_pattern.match(features['TRANSMISSION']):
                errors.append(f"Invalid transmission format: {features['TRANSMISSION']}")
        
        return len(errors) == 0, errors
    
    def create_feature_dataframe(self, features: Dict) -> pd.DataFrame:
        """Create pandas DataFrame from processed features"""
        try:
            df = pd.DataFrame([features])
            logger.info(f"📊 Created DataFrame with shape: {df.shape}")
            logger.info(f"📊 DataFrame columns: {list(df.columns)}")
            return df
            
        except Exception as e:
            logger.error(f"❌ DataFrame creation error: {str(e)}")
            raise ValueError(f"Failed to create feature DataFrame: {str(e)}")
    
    def get_feature_info(self) -> Dict:
        """Get information about feature processing capabilities"""
        return {
            'required_features': ['make', 'model', 'vehicle_class', 'engine_size', 
                                'cylinders', 'transmission', 'fuel_type'],
            'processed_features': ['MAKE', 'MODEL', 'VEHICLE CLASS', 'ENGINE SIZE', 
                                 'CYLINDERS', 'TRANSMISSION', 'FUEL'],
            'vehicle_classes_supported': list(self.vehicle_class_mapping.keys()),
            'makes_standardized': list(self.make_standardization.keys()),
            'fuel_types_supported': ['X', 'Z', 'D', 'E'],
            'engine_size_range': [0.5, 8.0],
            'cylinders_range': [1, 12],
            'transmission_formats': ['A4-A10', 'M5-M7', 'AV', 'AS']
        }

# Global processor instance
_processor_instance = None

def get_feature_processor() -> FeatureProcessor:
    """Get global feature processor instance"""
    global _processor_instance
    if _processor_instance is None:
        _processor_instance = FeatureProcessor()
    return _processor_instance

def process_vehicle_data(vehicle_data: Dict) -> Dict:
    """Convenience function for processing vehicle data"""
    processor = get_feature_processor()
    return processor.process_vehicle_features(vehicle_data)