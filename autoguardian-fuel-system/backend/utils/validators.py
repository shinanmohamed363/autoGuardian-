"""
AutoGuardian Fuel Management System - Validation Utilities
"""

import re
from typing import List, Dict, Any
from datetime import datetime, date

def validate_email(email: str) -> bool:
    """Validate email format"""
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email.strip()) is not None

def validate_password(password: str) -> List[str]:
    """Validate password strength and return list of errors"""
    errors = []
    
    if not password or not isinstance(password, str):
        errors.append("Password is required")
        return errors
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if len(password) > 128:
        errors.append("Password must be no more than 128 characters long")
    
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one number")
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password):
        errors.append("Password must contain at least one special character")
    
    return errors

def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> List[str]:
    """Validate that all required fields are present and not empty"""
    missing_fields = []
    
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
        elif data[field] is None or (isinstance(data[field], str) and data[field].strip() == ''):
            missing_fields.append(field)
    
    return missing_fields

def validate_vehicle_id(vehicle_id: str) -> bool:
    """Validate vehicle ID format"""
    if not vehicle_id or not isinstance(vehicle_id, str):
        return False
    
    # Vehicle ID should be alphanumeric with underscores, 3-50 characters
    pattern = r'^[a-zA-Z0-9_]{3,50}$'
    return re.match(pattern, vehicle_id.strip()) is not None

def validate_odometer_reading(current_reading: int, previous_reading: int = None) -> List[str]:
    """Validate odometer reading"""
    errors = []
    
    if not isinstance(current_reading, int) or current_reading < 0:
        errors.append("Odometer reading must be a positive integer")
        return errors
    
    if current_reading > 999999:
        errors.append("Odometer reading seems unreasonably high (max: 999,999)")
    
    if previous_reading is not None:
        if current_reading < previous_reading:
            errors.append(f"Odometer reading ({current_reading}) cannot be less than previous reading ({previous_reading})")
        elif current_reading - previous_reading > 10000:
            errors.append("Distance driven since last record seems unusually high (>10,000 km)")
    
    return errors

def validate_fuel_percentage(percentage: float) -> List[str]:
    """Validate fuel percentage"""
    errors = []
    
    if not isinstance(percentage, (int, float)):
        errors.append("Fuel percentage must be a number")
        return errors
    
    if percentage < 0 or percentage > 100:
        errors.append("Fuel percentage must be between 0 and 100")
    
    return errors

def validate_fuel_record(data: Dict[str, Any]) -> List[str]:
    """Validate fuel record data"""
    errors = []
    
    # Required fields
    required_fields = [
        'vehicle_id', 'record_date', 'record_time',
        'existing_tank_percentage', 'after_refuel_percentage',
        'odo_meter_current_value', 'driving_type', 'location', 'fuel_price'
    ]
    
    missing_fields = validate_required_fields(data, required_fields)
    errors.extend([f"Missing required field: {field}" for field in missing_fields])
    
    if missing_fields:
        return errors  # Return early if required fields are missing
    
    # Validate vehicle ID (should be integer)
    try:
        vehicle_id = int(data['vehicle_id'])
        if vehicle_id <= 0:
            errors.append("Vehicle ID must be a positive integer")
    except (ValueError, TypeError):
        errors.append("Invalid vehicle ID format")
    
    # Validate date
    try:
        if isinstance(data['record_date'], str):
            datetime.strptime(data['record_date'], '%Y-%m-%d')
        elif not isinstance(data['record_date'], date):
            errors.append("Invalid date format (expected YYYY-MM-DD)")
    except ValueError:
        errors.append("Invalid date format (expected YYYY-MM-DD)")
    
    # Validate time
    try:
        if isinstance(data['record_time'], str):
            datetime.strptime(data['record_time'], '%H:%M')
    except ValueError:
        errors.append("Invalid time format (expected HH:MM)")
    
    # Validate fuel percentages
    existing_errors = validate_fuel_percentage(data['existing_tank_percentage'])
    errors.extend([f"Existing tank percentage: {error}" for error in existing_errors])
    
    after_errors = validate_fuel_percentage(data['after_refuel_percentage'])
    errors.extend([f"After refuel percentage: {error}" for error in after_errors])
    
    # Check that after_refuel > existing
    if (not existing_errors and not after_errors and 
        data['after_refuel_percentage'] <= data['existing_tank_percentage']):
        errors.append("After refuel percentage must be greater than existing tank percentage")
    
    # Validate odometer
    odometer_errors = validate_odometer_reading(data['odo_meter_current_value'])
    errors.extend(odometer_errors)
    
    # Validate driving type
    valid_driving_types = ['city', 'highway', 'mix']
    if data['driving_type'] not in valid_driving_types:
        errors.append(f"Driving type must be one of: {valid_driving_types}")
    
    # Validate location
    if not data['location'] or len(data['location'].strip()) < 2:
        errors.append("Location must be at least 2 characters long")
    elif len(data['location']) > 100:
        errors.append("Location must be no more than 100 characters long")
    
    # Validate fuel price
    if not isinstance(data['fuel_price'], (int, float)) or data['fuel_price'] <= 0:
        errors.append("Fuel price must be a positive number")
    elif data['fuel_price'] > 1000:  # Assuming price in cents per liter
        errors.append("Fuel price seems unreasonably high")
    
    return errors

def validate_vehicle_data(data: Dict[str, Any]) -> List[str]:
    """Validate vehicle data"""
    errors = []
    
    # Required fields (removed vehicle_id since it's auto-generated)
    required_fields = [
        'vehicle_name', 'make', 'model', 'year',
        'vehicle_class', 'engine_size', 'cylinders', 'transmission',
        'fuel_type', 'tank_capacity', 'full_tank_capacity'
    ]
    
    missing_fields = validate_required_fields(data, required_fields)
    errors.extend([f"Missing required field: {field}" for field in missing_fields])
    
    if missing_fields:
        return errors
    
    # No need to validate vehicle_id since it's auto-generated
    
    # Validate vehicle name
    if len(data['vehicle_name'].strip()) < 2:
        errors.append("Vehicle name must be at least 2 characters long")
    elif len(data['vehicle_name']) > 100:
        errors.append("Vehicle name must be no more than 100 characters long")
    
    # Validate make and model
    for field in ['make', 'model']:
        if len(data[field].strip()) < 1:
            errors.append(f"{field.capitalize()} is required")
        elif len(data[field]) > 50:
            errors.append(f"{field.capitalize()} must be no more than 50 characters long")
    
    # Validate year
    current_year = datetime.now().year
    if not isinstance(data['year'], int) or data['year'] < 1900 or data['year'] > current_year + 2:
        errors.append(f"Year must be between 1900 and {current_year + 2}")
    
    # Validate engine size
    try:
        engine_size = float(data['engine_size']) if not isinstance(data['engine_size'], float) else data['engine_size']
        if engine_size < 0.5 or engine_size > 8.0:
            errors.append("Engine size must be between 0.5L and 8.0L")
    except (ValueError, TypeError):
        errors.append("Engine size must be a valid number")
    
    # Validate cylinders
    if not isinstance(data['cylinders'], int) or data['cylinders'] < 1 or data['cylinders'] > 12:
        errors.append("Cylinders must be between 1 and 12")
    
    # Validate tank capacities
    for capacity_field in ['tank_capacity', 'full_tank_capacity']:
        try:
            capacity = float(data[capacity_field])
            if capacity < 20 or capacity > 200:
                errors.append(f"{capacity_field.replace('_', ' ').title()} must be between 20L and 200L")
        except (ValueError, TypeError):
            errors.append(f"{capacity_field.replace('_', ' ').title()} must be a valid number")
    
    # Validate vehicle class
    if len(data['vehicle_class']) > 50:
        errors.append("Vehicle class must be no more than 50 characters long")
    
    # Validate transmission
    if len(data['transmission']) > 20:
        errors.append("Transmission must be no more than 20 characters long")
    
    # Validate fuel type
    if len(data['fuel_type']) > 20:
        errors.append("Fuel type must be no more than 20 characters long")
    
    return errors

def validate_date_range(start_date: str, end_date: str) -> List[str]:
    """Validate date range"""
    errors = []
    
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        if start > end:
            errors.append("Start date must be before or equal to end date")
        
        if start > date.today():
            errors.append("Start date cannot be in the future")
        
        # Check if date range is too large (e.g., more than 2 years)
        if (end - start).days > 730:
            errors.append("Date range cannot exceed 2 years")
            
    except ValueError:
        errors.append("Invalid date format (expected YYYY-MM-DD)")
    
    return errors

def sanitize_string(value: str, max_length: int = None) -> str:
    """Sanitize string input"""
    if not value or not isinstance(value, str):
        return ""
    
    # Strip whitespace and normalize
    sanitized = value.strip()
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', sanitized)
    
    # Truncate if needed
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized

def validate_pagination(page: int, per_page: int) -> List[str]:
    """Validate pagination parameters"""
    errors = []
    
    if not isinstance(page, int) or page < 1:
        errors.append("Page must be a positive integer")
    
    if not isinstance(per_page, int) or per_page < 1 or per_page > 100:
        errors.append("Per page must be between 1 and 100")
    
    return errors