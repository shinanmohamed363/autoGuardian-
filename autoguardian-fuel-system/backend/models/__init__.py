"""
AutoGuardian Fuel Management System - Database Models Package
"""

from database import db

# Import all models to ensure they're registered with SQLAlchemy
from .user import User, UserPreferences
from .vehicle import Vehicle, VehicleStatistics
from .fuel_record import FuelRecord
from .predictions import MLPrediction
from .recommendations import AIRecommendation

__all__ = [
    'User', 'UserPreferences',
    'Vehicle', 'VehicleStatistics', 
    'FuelRecord',
    'MLPrediction',
    'AIRecommendation'
]