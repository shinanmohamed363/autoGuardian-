"""
AutoGuardian Fuel Management System - Routes Package
"""

# Import all route blueprints for easy access
from .auth import auth_bp
from .vehicles import vehicles_bp
from .fuel_records import fuel_records_bp
from .predictions import predictions_bp
from .recommendations import recommendations_bp
from .analytics import analytics_bp

__all__ = [
    'auth_bp',
    'vehicles_bp', 
    'fuel_records_bp',
    'predictions_bp',
    'recommendations_bp',
    'analytics_bp'
]