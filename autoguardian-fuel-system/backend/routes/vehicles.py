"""
AutoGuardian Fuel Management System - Vehicle Routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from database import db
from models.vehicle import Vehicle, VehicleStatistics
from models.user import User
from utils.validators import validate_vehicle_data, validate_required_fields
from ml_models.model_handler import get_predictor

# Create vehicles blueprint
vehicles_bp = Blueprint('vehicles', __name__)

@vehicles_bp.route('', methods=['POST'])
@jwt_required()
def create_vehicle():
    """Create a new vehicle"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        # Validate input data
        validation_errors = validate_vehicle_data(data)
        if validation_errors:
            return jsonify({
                'error': 'Validation failed',
                'validation_errors': validation_errors
            }), 400
        
        # No need to check for duplicate vehicle_id since we use auto-generated ID
        
        # Create new vehicle
        vehicle = Vehicle(
            user_id=current_user_id,
            vehicle_name=data['vehicle_name'],
            make=data['make'],
            model=data['model'],
            year=data['year'],
            vehicle_class=data['vehicle_class'],
            engine_size=data['engine_size'],
            cylinders=data['cylinders'],
            transmission=data['transmission'],
            fuel_type=data['fuel_type'],
            tank_capacity=data['tank_capacity'],
            starting_odometer_value=data.get('starting_odometer_value', 0),
            odo_meter_when_buy_vehicle=data.get('odo_meter_when_buy_vehicle'),
            full_tank_capacity=data.get('full_tank_capacity', data['tank_capacity']),
            initial_tank_percentage=data.get('initial_tank_percentage', 100.0)
        )
        
        db.session.add(vehicle)
        db.session.commit()
        
        # Create vehicle statistics
        stats = VehicleStatistics(vehicle_id=vehicle.id)
        db.session.add(stats)
        db.session.commit()
        
        return jsonify({
            'message': 'Vehicle created successfully',
            'vehicle': vehicle.to_dict(include_stats=False)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Vehicle creation failed', 'message': str(e)}), 500

@vehicles_bp.route('', methods=['GET'])
@jwt_required()
def get_vehicles():
    """Get all vehicles for current user"""
    try:
        current_user_id = int(get_jwt_identity())
        vehicles = Vehicle.find_by_user(current_user_id)
        
        vehicles_data = []
        for vehicle in vehicles:
            vehicle_dict = vehicle.to_dict(include_stats=True)
            vehicles_data.append(vehicle_dict)
        
        return jsonify({
            'vehicles': vehicles_data,
            'count': len(vehicles_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get vehicles', 'message': str(e)}), 500

@vehicles_bp.route('/<int:vehicle_id>', methods=['GET'])
@jwt_required()
def get_vehicle(vehicle_id):
    """Get specific vehicle"""
    try:
        current_user_id = int(get_jwt_identity())
        vehicle = Vehicle.find_by_id(vehicle_id)
        
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        
        if vehicle.user_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        return jsonify({
            'vehicle': vehicle.to_dict(include_stats=True)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get vehicle', 'message': str(e)}), 500

@vehicles_bp.route('/<int:vehicle_id>', methods=['PUT'])
@jwt_required()
def update_vehicle(vehicle_id):
    """Update vehicle"""
    try:
        current_user_id = int(get_jwt_identity())
        vehicle = Vehicle.find_by_id(vehicle_id)
        
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        
        if vehicle.user_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        # Update allowed fields
        updatable_fields = [
            'vehicle_name', 'make', 'model', 'year', 'vehicle_class',
            'engine_size', 'cylinders', 'transmission', 'fuel_type',
            'tank_capacity', 'full_tank_capacity'
        ]
        
        updated_fields = []
        for field in updatable_fields:
            if field in data:
                setattr(vehicle, field, data[field])
                updated_fields.append(field)
        
        vehicle.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Vehicle updated successfully',
            'updated_fields': updated_fields,
            'vehicle': vehicle.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Vehicle update failed', 'message': str(e)}), 500

@vehicles_bp.route('/<int:vehicle_id>', methods=['DELETE'])
@jwt_required()
def delete_vehicle(vehicle_id):
    """Delete vehicle"""
    try:
        current_user_id = int(get_jwt_identity())
        vehicle = Vehicle.find_by_id(vehicle_id)
        
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        
        if vehicle.user_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        vehicle.is_active = False
        vehicle.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': 'Vehicle deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Vehicle deletion failed', 'message': str(e)}), 500

@vehicles_bp.route('/<int:vehicle_id>/predict', methods=['POST'])
@jwt_required()
def predict_vehicle_fuel(vehicle_id):
    """Generate ML prediction for vehicle"""
    try:
        current_user_id = int(get_jwt_identity())
        vehicle = Vehicle.find_by_id(vehicle_id)
        
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        
        if vehicle.user_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Get ML prediction
        predictor = get_predictor()
        vehicle_data = vehicle.get_ml_prediction_features()
        prediction = predictor.predict(vehicle_data)
        
        return jsonify({
            'vehicle_id': vehicle_id,
            'prediction': prediction
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Prediction failed', 'message': str(e)}), 500