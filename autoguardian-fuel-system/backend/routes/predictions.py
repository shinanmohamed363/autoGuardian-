"""
AutoGuardian Fuel Management System - ML Predictions Routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database import db
from models.vehicle import Vehicle
from models.predictions import MLPrediction
from models.user import User
from ml_models.model_handler import get_predictor
from utils.validators import validate_required_fields

# Create predictions blueprint
predictions_bp = Blueprint('predictions', __name__)

@predictions_bp.route('', methods=['POST'])
@jwt_required()
def generate_prediction():
    """Generate ML prediction for a vehicle"""
    try:
        current_user_id = int(get_jwt_identity())
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        required_fields = ['vehicle_id']
        missing_fields = validate_required_fields(data, required_fields)
        if missing_fields:
            return jsonify({'error': 'Missing required fields', 'missing_fields': missing_fields}), 400
        
        vehicle_id = data['vehicle_id']
        
        
        # Check if user owns the vehicle
        vehicle = Vehicle.find_by_id(vehicle_id)
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        
        if vehicle.user_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Get predictor and make prediction
        predictor = get_predictor()
        if not predictor.is_loaded:
            return jsonify({'error': 'ML model not available'}), 503
        
        # Get vehicle features for prediction
        vehicle_features = vehicle.get_ml_prediction_features()
        
        # Make prediction
        prediction_result = predictor.predict(vehicle_features)
        
        # TODO: Save prediction to database (skipped due to schema issues)
        # For now, just return the prediction without saving
        
        return jsonify({
            'message': 'ML prediction generated successfully',
            'prediction': prediction_result,
            'vehicle_id': vehicle_id,
            'vehicle_info': {
                'make': vehicle.make,
                'model': vehicle.model,
                'year': vehicle.year,
                'engine_info': vehicle.engine_info
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Prediction failed', 'message': str(e)}), 500

@predictions_bp.route('/<vehicle_id>', methods=['GET'])
@jwt_required()
def get_vehicle_predictions(vehicle_id):
    """Get prediction history for a vehicle"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # Check if user owns the vehicle
        vehicle = Vehicle.find_by_id(vehicle_id)
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        
        if vehicle.user_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Get query parameters
        limit = request.args.get('limit', 10, type=int)
        
        # Get predictions
        predictions = MLPrediction.get_prediction_history(vehicle_id, limit=limit)
        
        predictions_data = []
        for prediction in predictions:
            predictions_data.append(prediction.to_dict(include_analysis=True))
        
        return jsonify({
            'predictions': predictions_data,
            'count': len(predictions_data),
            'vehicle_id': vehicle_id
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get predictions', 'message': str(e)}), 500

@predictions_bp.route('/latest/<vehicle_id>', methods=['GET'])
@jwt_required()
def get_latest_prediction(vehicle_id):
    """Get latest prediction for a vehicle"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # Check if user owns the vehicle
        vehicle = Vehicle.find_by_id(vehicle_id)
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        
        if vehicle.user_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Get latest prediction
        prediction = MLPrediction.get_latest_prediction(vehicle_id)
        
        if not prediction:
            return jsonify({'error': 'No predictions found for this vehicle'}), 404
        
        return jsonify({
            'prediction': prediction.to_dict(include_analysis=True),
            'vehicle_id': vehicle_id
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get prediction', 'message': str(e)}), 500

@predictions_bp.route('/batch', methods=['POST'])
@jwt_required()
def batch_predictions():
    """Generate predictions for multiple vehicles"""
    try:
        current_user_id = int(get_jwt_identity())
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        required_fields = ['vehicle_ids']
        missing_fields = validate_required_fields(data, required_fields)
        if missing_fields:
            return jsonify({'error': 'Missing required fields', 'missing_fields': missing_fields}), 400
        
        vehicle_ids = data['vehicle_ids']
        if not isinstance(vehicle_ids, list) or len(vehicle_ids) == 0:
            return jsonify({'error': 'vehicle_ids must be a non-empty list'}), 400
        
        if len(vehicle_ids) > 10:  # Limit batch size
            return jsonify({'error': 'Maximum 10 vehicles allowed per batch'}), 400
        
        # Get predictor
        predictor = get_predictor()
        if not predictor.is_loaded:
            return jsonify({'error': 'ML model not available'}), 503
        
        results = []
        
        for vehicle_id in vehicle_ids:
            try:
                # Check if user owns the vehicle
                vehicle = Vehicle.find_by_id(vehicle_id)
                if not vehicle or vehicle.user_id != current_user_id:
                    results.append({
                        'vehicle_id': vehicle_id,
                        'error': 'Vehicle not found or access denied',
                        'success': False
                    })
                    continue
                
                # Get vehicle features and make prediction
                vehicle_features = vehicle.get_ml_prediction_features()
                prediction_result = predictor.predict(vehicle_features)
                
                # Save prediction to database (only use core fields)
                ml_prediction = MLPrediction(
                    vehicle_id=vehicle_id,
                    combined_l_100km=prediction_result['combined_l_100km']
                )
                
                db.session.add(ml_prediction)
                
                results.append({
                    'vehicle_id': vehicle_id,
                    'prediction': prediction_result,
                    'vehicle_info': {
                        'make': vehicle.make,
                        'model': vehicle.model,
                        'year': vehicle.year
                    },
                    'success': True
                })
                
            except Exception as e:
                results.append({
                    'vehicle_id': vehicle_id,
                    'error': str(e),
                    'success': False
                })
        
        db.session.commit()
        
        successful_predictions = sum(1 for r in results if r.get('success'))
        
        return jsonify({
            'results': results,
            'total_requested': len(vehicle_ids),
            'successful_predictions': successful_predictions,
            'failed_predictions': len(vehicle_ids) - successful_predictions
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Batch prediction failed', 'message': str(e)}), 500

@predictions_bp.route('/model/info', methods=['GET'])
@jwt_required()
def get_model_info():
    """Get ML model information"""
    try:
        predictor = get_predictor()
        model_info = predictor.get_model_info()
        
        return jsonify({
            'model_info': model_info
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get model info', 'message': str(e)}), 500

@predictions_bp.route('/validate', methods=['POST'])
@jwt_required()
def validate_prediction_input():
    """Validate vehicle data for prediction"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        predictor = get_predictor()
        is_valid, validation_errors = predictor.validate_input(data)
        
        if is_valid:
            return jsonify({
                'valid': True,
                'message': 'Vehicle data is valid for prediction'
            }), 200
        else:
            return jsonify({
                'valid': False,
                'validation_errors': validation_errors
            }), 400
        
    except Exception as e:
        return jsonify({'error': 'Validation failed', 'message': str(e)}), 500