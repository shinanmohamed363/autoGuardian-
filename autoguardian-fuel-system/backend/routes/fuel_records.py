"""
AutoGuardian Fuel Management System - Fuel Records Routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date

from database import db
from models.fuel_record import FuelRecord
from models.vehicle import Vehicle
from models.user import User
from utils.validators import validate_fuel_record, validate_required_fields

# Create fuel records blueprint
fuel_records_bp = Blueprint('fuel_records', __name__)

@fuel_records_bp.route('', methods=['POST'])
@jwt_required()
def create_fuel_record():
    """Create a new fuel record"""
    try:
        current_user_id = int(get_jwt_identity())
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        # Validate input data
        validation_errors = validate_fuel_record(data)
        if validation_errors:
            return jsonify({
                'error': 'Validation failed',
                'validation_errors': validation_errors
            }), 400
        
        # Check if user owns the vehicle
        vehicle = Vehicle.find_by_id(data['vehicle_id'])
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        
        if vehicle.user_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Validate odometer reading against previous records
        is_valid, error_msg = FuelRecord.validate_new_odometer(
            data['vehicle_id'], data['odo_meter_current_value']
        )
        
        if not is_valid:
            return jsonify({'error': 'Invalid odometer reading', 'message': error_msg}), 400
        
        # Create new fuel record
        fuel_record = FuelRecord(
            vehicle_id=data['vehicle_id'],
            record_date=data['record_date'],
            record_time=data['record_time'],
            existing_tank_percentage=data['existing_tank_percentage'],
            after_refuel_percentage=data['after_refuel_percentage'],
            odo_meter_current_value=data['odo_meter_current_value'],
            driving_type=data['driving_type'],
            location=data['location'],
            fuel_price=data['fuel_price'],
            notes=data.get('notes')
        )
        
        db.session.add(fuel_record)
        db.session.commit()
        
        return jsonify({
            'message': 'Fuel record created successfully',
            'fuel_record': fuel_record.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Fuel record creation failed', 'message': str(e)}), 500

@fuel_records_bp.route('/<vehicle_id>', methods=['GET'])
@jwt_required()
def get_fuel_records(vehicle_id):
    """Get fuel records for a vehicle"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # Check if user owns the vehicle
        vehicle = Vehicle.find_by_id(vehicle_id)
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        
        if vehicle.user_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Get query parameters
        limit = request.args.get('limit', type=int)
        days = request.args.get('days', type=int)
        
        # Get fuel records
        fuel_records = FuelRecord.get_vehicle_records(vehicle_id, limit=limit, days=days)
        
        records_data = []
        for record in fuel_records:
            records_data.append(record.to_dict())
        
        return jsonify({
            'fuel_records': records_data,
            'count': len(records_data),
            'vehicle_id': vehicle_id
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get fuel records', 'message': str(e)}), 500

@fuel_records_bp.route('/record/<int:record_id>', methods=['GET'])
@jwt_required()
def get_fuel_record(record_id):
    """Get specific fuel record"""
    try:
        current_user_id = int(get_jwt_identity())
        
        fuel_record = FuelRecord.query.get(record_id)
        if not fuel_record:
            return jsonify({'error': 'Fuel record not found'}), 404
        
        # Check if user owns the vehicle
        vehicle = Vehicle.find_by_id(fuel_record.vehicle_id)
        if not vehicle or vehicle.user_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        return jsonify({
            'fuel_record': fuel_record.to_dict(include_analysis=True)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get fuel record', 'message': str(e)}), 500

@fuel_records_bp.route('/record/<int:record_id>', methods=['PUT'])
@jwt_required()
def update_fuel_record(record_id):
    """Update fuel record"""
    try:
        current_user_id = int(get_jwt_identity())
        
        fuel_record = FuelRecord.query.get(record_id)
        if not fuel_record:
            return jsonify({'error': 'Fuel record not found'}), 404
        
        # Check if user owns the vehicle
        vehicle = Vehicle.find_by_id(fuel_record.vehicle_id)
        if not vehicle or vehicle.user_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        # Update allowed fields
        updatable_fields = [
            'record_date', 'record_time', 'existing_tank_percentage',
            'after_refuel_percentage', 'odo_meter_current_value',
            'driving_type', 'location', 'fuel_price', 'notes'
        ]
        
        updated_fields = []
        for field in updatable_fields:
            if field in data:
                if field == 'record_date' and isinstance(data[field], str):
                    setattr(fuel_record, field, datetime.strptime(data[field], '%Y-%m-%d').date())
                elif field == 'record_time' and isinstance(data[field], str):
                    setattr(fuel_record, field, datetime.strptime(data[field], '%H:%M').time())
                else:
                    setattr(fuel_record, field, data[field])
                updated_fields.append(field)
        
        # Recalculate metrics
        fuel_record.recalculate_metrics()
        fuel_record.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Fuel record updated successfully',
            'updated_fields': updated_fields,
            'fuel_record': fuel_record.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Fuel record update failed', 'message': str(e)}), 500

@fuel_records_bp.route('/record/<int:record_id>', methods=['DELETE'])
@jwt_required()
def delete_fuel_record(record_id):
    """Delete fuel record"""
    try:
        current_user_id = int(get_jwt_identity())
        
        fuel_record = FuelRecord.query.get(record_id)
        if not fuel_record:
            return jsonify({'error': 'Fuel record not found'}), 404
        
        # Check if user owns the vehicle
        vehicle = Vehicle.find_by_id(fuel_record.vehicle_id)
        if not vehicle or vehicle.user_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        db.session.delete(fuel_record)
        db.session.commit()
        
        return jsonify({'message': 'Fuel record deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Fuel record deletion failed', 'message': str(e)}), 500

@fuel_records_bp.route('/validate-odometer', methods=['POST'])
@jwt_required()
def validate_odometer():
    """Validate odometer reading"""
    try:
        current_user_id = int(get_jwt_identity())
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        required_fields = ['vehicle_id', 'odometer_reading']
        missing_fields = validate_required_fields(data, required_fields)
        if missing_fields:
            return jsonify({'error': 'Missing required fields', 'missing_fields': missing_fields}), 400
        
        # Check if user owns the vehicle
        vehicle = Vehicle.find_by_id(data['vehicle_id'])
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        
        if vehicle.user_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Validate odometer reading
        is_valid, error_msg = FuelRecord.validate_new_odometer(
            data['vehicle_id'], data['odometer_reading']
        )
        
        if is_valid:
            return jsonify({
                'valid': True,
                'message': 'Odometer reading is valid'
            }), 200
        else:
            return jsonify({
                'valid': False,
                'message': error_msg
            }), 400
        
    except Exception as e:
        return jsonify({'error': 'Validation failed', 'message': str(e)}), 500