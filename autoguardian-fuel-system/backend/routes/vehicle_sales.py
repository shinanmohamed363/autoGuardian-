"""
AutoGuardian Fuel Management System - Vehicle Sales Routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError

from database import db
from models.vehicle_sale import VehicleSale, Negotiation
from models.vehicle import Vehicle
from models.user import User
from utils.validators import validate_required_fields
from services.negotiation_bot import NegotiationBot

# Create vehicle sales blueprint
vehicle_sales_bp = Blueprint('vehicle_sales', __name__)

# Initialize negotiation bot
negotiation_bot = NegotiationBot()

@vehicle_sales_bp.route('', methods=['POST'])
@jwt_required()
def create_vehicle_sale():
    """Create a new vehicle sale listing"""
    try:
        current_user_id = int(get_jwt_identity())
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        required_fields = ['vehicle_id', 'selling_price', 'minimum_price']
        missing_fields = validate_required_fields(data, required_fields)
        if missing_fields:
            return jsonify({'error': 'Missing required fields', 'missing_fields': missing_fields}), 400
        
        vehicle_id = data['vehicle_id']
        selling_price = float(data['selling_price'])
        minimum_price = float(data['minimum_price'])
        features = data.get('features', [])
        description = data.get('description', '')
        
        # Validate prices
        if selling_price <= 0 or minimum_price <= 0:
            return jsonify({'error': 'Prices must be positive numbers'}), 400
        
        if minimum_price > selling_price:
            return jsonify({'error': 'Minimum price cannot be higher than selling price'}), 400
        
        # Check if user owns the vehicle
        vehicle = Vehicle.find_by_id(vehicle_id)
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        
        if vehicle.user_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Check if vehicle is already listed for sale
        existing_sale = VehicleSale.query.filter_by(
            vehicle_id=vehicle_id, 
            is_active=True, 
            is_sold=False
        ).first()
        
        if existing_sale:
            return jsonify({'error': 'Vehicle is already listed for sale'}), 400
        
        # Create new sale listing
        vehicle_sale = VehicleSale(
            user_id=current_user_id,
            vehicle_id=vehicle_id,
            selling_price=selling_price,
            minimum_price=minimum_price,
            features=features,
            description=description
        )
        
        db.session.add(vehicle_sale)
        db.session.commit()
        
        return jsonify({
            'message': 'Vehicle listed for sale successfully',
            'vehicle_sale': vehicle_sale.to_dict(include_sensitive=True)
        }), 201
        
    except ValueError as e:
        return jsonify({'error': 'Invalid price format'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create vehicle sale', 'message': str(e)}), 500

@vehicle_sales_bp.route('', methods=['GET'])
def get_vehicle_sales():
    """Get all active vehicle sales (public endpoint)"""
    try:
        # Check if user is authenticated (optional for this endpoint)
        current_user_id = None
        try:
            verify_jwt_in_request(optional=True)
            if get_jwt_identity():
                current_user_id = int(get_jwt_identity())
        except NoAuthorizationError:
            pass
        
        # Get query parameters
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Get active sales excluding current user's sales
        sales_query = VehicleSale.query.filter_by(is_active=True, is_sold=False)
        if current_user_id:
            sales_query = sales_query.filter(VehicleSale.user_id != current_user_id)
        
        # Apply pagination
        sales = sales_query.limit(limit).offset(offset).all()
        
        # Get vehicle details for each sale
        sales_data = []
        for sale in sales:
            sale_dict = sale.to_dict()
            # Add vehicle details
            vehicle = Vehicle.find_by_id(sale.vehicle_id)
            if vehicle:
                sale_dict['vehicle'] = {
                    'vehicle_name': vehicle.vehicle_name,
                    'make': vehicle.make,
                    'model': vehicle.model,
                    'year': vehicle.year,
                    'vehicle_class': vehicle.vehicle_class,
                    'engine_size': vehicle.engine_size,
                    'fuel_type': vehicle.fuel_type,
                    'transmission': vehicle.transmission,
                    'current_odometer': vehicle.current_odometer,
                    'tank_capacity': vehicle.tank_capacity
                }
            sales_data.append(sale_dict)
        
        return jsonify({
            'vehicle_sales': sales_data,
            'count': len(sales_data),
            'has_more': len(sales) == limit
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get vehicle sales', 'message': str(e)}), 500

@vehicle_sales_bp.route('/my-sales', methods=['GET'])
@jwt_required()
def get_my_vehicle_sales():
    """Get current user's vehicle sales"""
    try:
        current_user_id = int(get_jwt_identity())
        
        # Get user's sales
        sales = VehicleSale.get_user_sales(current_user_id)
        
        sales_data = []
        for sale in sales:
            sale_dict = sale.to_dict(include_sensitive=True)
            # Add vehicle details
            vehicle = Vehicle.find_by_id(sale.vehicle_id)
            if vehicle:
                sale_dict['vehicle'] = vehicle.to_dict()
            
            # Add negotiation count
            negotiations_count = Negotiation.query.filter_by(vehicle_sale_id=sale.id).count()
            sale_dict['negotiations_count'] = negotiations_count
            
            sales_data.append(sale_dict)
        
        return jsonify({
            'vehicle_sales': sales_data,
            'count': len(sales_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get user vehicle sales', 'message': str(e)}), 500

@vehicle_sales_bp.route('/<int:sale_id>', methods=['GET'])
def get_vehicle_sale(sale_id):
    """Get specific vehicle sale details"""
    try:
        # Check if user is authenticated
        current_user_id = None
        is_owner = False
        try:
            verify_jwt_in_request(optional=True)
            if get_jwt_identity():
                current_user_id = int(get_jwt_identity())
        except NoAuthorizationError:
            pass
        
        vehicle_sale = VehicleSale.find_by_id(sale_id)
        if not vehicle_sale:
            return jsonify({'error': 'Vehicle sale not found'}), 404
        
        if not vehicle_sale.is_active:
            return jsonify({'error': 'Vehicle sale is no longer active'}), 404
        
        # Check if current user is the owner
        is_owner = current_user_id == vehicle_sale.user_id
        
        # Get sale details
        sale_dict = vehicle_sale.to_dict(include_sensitive=is_owner)
        
        # Add vehicle details
        vehicle = Vehicle.find_by_id(vehicle_sale.vehicle_id)
        if vehicle:
            sale_dict['vehicle'] = {
                'vehicle_name': vehicle.vehicle_name,
                'make': vehicle.make,
                'model': vehicle.model,
                'year': vehicle.year,
                'vehicle_class': vehicle.vehicle_class,
                'engine_size': vehicle.engine_size,
                'fuel_type': vehicle.fuel_type,
                'transmission': vehicle.transmission,
                'current_odometer': vehicle.current_odometer,
                'tank_capacity': vehicle.tank_capacity,
                'cylinders': vehicle.cylinders
            }
        
        # Add seller info (limited)
        seller = User.query.get(vehicle_sale.user_id)
        if seller:
            sale_dict['seller'] = {
                'name': f"{seller.first_name} {seller.last_name}",
                'location': 'Colombo, Sri Lanka'  # Default location
            }
        
        return jsonify({
            'vehicle_sale': sale_dict
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get vehicle sale', 'message': str(e)}), 500

@vehicle_sales_bp.route('/<int:sale_id>', methods=['PUT'])
@jwt_required()
def update_vehicle_sale(sale_id):
    """Update vehicle sale"""
    try:
        current_user_id = int(get_jwt_identity())
        
        vehicle_sale = VehicleSale.find_by_id(sale_id)
        if not vehicle_sale:
            return jsonify({'error': 'Vehicle sale not found'}), 404
        
        if vehicle_sale.user_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        # Update allowed fields
        allowed_fields = ['selling_price', 'minimum_price', 'features', 'description', 'is_active']
        update_data = {k: v for k, v in data.items() if k in allowed_fields}
        
        # Validate prices if provided
        if 'selling_price' in update_data or 'minimum_price' in update_data:
            selling_price = float(update_data.get('selling_price', vehicle_sale.selling_price))
            minimum_price = float(update_data.get('minimum_price', vehicle_sale.minimum_price))
            
            if selling_price <= 0 or minimum_price <= 0:
                return jsonify({'error': 'Prices must be positive numbers'}), 400
            
            if minimum_price > selling_price:
                return jsonify({'error': 'Minimum price cannot be higher than selling price'}), 400
        
        # Update the sale
        vehicle_sale.update_sale(**update_data)
        
        return jsonify({
            'message': 'Vehicle sale updated successfully',
            'vehicle_sale': vehicle_sale.to_dict(include_sensitive=True)
        }), 200
        
    except ValueError as e:
        return jsonify({'error': 'Invalid price format'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update vehicle sale', 'message': str(e)}), 500

@vehicle_sales_bp.route('/<int:sale_id>', methods=['DELETE'])
@jwt_required()
def delete_vehicle_sale(sale_id):
    """Delete/deactivate vehicle sale"""
    try:
        current_user_id = int(get_jwt_identity())
        
        vehicle_sale = VehicleSale.find_by_id(sale_id)
        if not vehicle_sale:
            return jsonify({'error': 'Vehicle sale not found'}), 404
        
        if vehicle_sale.user_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Deactivate instead of deleting
        vehicle_sale.deactivate_sale()
        
        return jsonify({
            'message': 'Vehicle sale deactivated successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete vehicle sale', 'message': str(e)}), 500

@vehicle_sales_bp.route('/<int:sale_id>/negotiate', methods=['POST'])
def negotiate_price(sale_id):
    """Start or continue price negotiation (public endpoint)"""
    try:
        vehicle_sale = VehicleSale.find_by_id(sale_id)
        if not vehicle_sale:
            return jsonify({'error': 'Vehicle sale not found'}), 404
        
        if not vehicle_sale.is_active or vehicle_sale.is_sold:
            return jsonify({'error': 'Vehicle is no longer available'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        message = data.get('message', '').strip()
        negotiation_id = data.get('negotiation_id')  # Optional, for continuing negotiation
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get or create negotiation
        negotiation = None
        negotiation_round = 0
        
        if negotiation_id:
            # Continue existing negotiation
            negotiation = Negotiation.find_by_id(negotiation_id)
            if not negotiation or negotiation.vehicle_sale_id != sale_id:
                return jsonify({'error': 'Invalid negotiation'}), 404
            
            negotiation_round = len([msg for msg in negotiation.chat_history 
                                   if msg.get('sender') == 'system']) if negotiation.chat_history else 0
        
        # Check if user is providing contact details (final step)
        contact_details = negotiation_bot.parse_contact_details(message)
        
        if contact_details and negotiation and negotiation.chat_history:
            # User provided contact details - finalize negotiation
            # Use the existing final_offer from negotiation, fallback to finding from chat if needed
            final_price = negotiation.final_offer if negotiation.final_offer > 0 else vehicle_sale.selling_price
            
            # If no final_offer was set during negotiation, try to extract from chat history
            if negotiation.final_offer == 0:
                for msg in reversed(negotiation.chat_history):
                    if msg.get('sender') == 'system' and 'final price' in msg.get('message', '').lower():
                        import re
                        price_match = re.search(r'Rs\.\s*([\d,]+)', msg['message'])
                        if price_match:
                            final_price = float(price_match.group(1).replace(',', ''))
                            break
                negotiation.final_offer = final_price
            
            # Update negotiation with contact details
            negotiation.buyer_name = contact_details['name']
            negotiation.buyer_email = contact_details['email']
            negotiation.buyer_contact = contact_details['phone']
            
            # Add contact message to history
            negotiation.add_chat_message('buyer', message)
            
            # Add system confirmation
            confirmation_msg = f"Thank you {contact_details['name']}! I have your details: Email: {contact_details['email']}"
            if contact_details['phone']:
                confirmation_msg += f", Phone: {contact_details['phone']}"
            confirmation_msg += f". The vehicle owner will contact you soon regarding the final price of Rs. {negotiation.final_offer:,.0f}."
            
            negotiation.add_chat_message('system', confirmation_msg)
            
            return jsonify({
                'message': 'Negotiation completed successfully',
                'negotiation': negotiation.to_dict(),
                'contact_collected': True,
                'final_price': negotiation.final_offer
            }), 200
        
        # Regular negotiation flow
        if not negotiation:
            # Create new negotiation
            negotiation = Negotiation(
                vehicle_sale_id=sale_id,
                buyer_name='Anonymous',  # Will be updated when contact details are provided
                buyer_email='',
                final_offer=0,  # Will be updated
                chat_history=[]
            )
            db.session.add(negotiation)
            db.session.flush()  # Get the ID without committing
        
        # Add user message to history
        negotiation.add_chat_message('buyer', message)
        
        # Generate bot response
        vehicle_data = {
            'selling_price': vehicle_sale.selling_price,
            'minimum_price': vehicle_sale.minimum_price,
            'features': vehicle_sale.features or []
        }
        
        bot_response, current_offer, is_final = negotiation_bot.generate_response(
            vehicle_data, message, negotiation.chat_history, negotiation_round
        )
        
        # Add bot response to history
        negotiation.add_chat_message('system', bot_response)
        
        # Update final_offer if this is a final offer or if it's a better deal than previous offers
        if is_final or negotiation.final_offer == 0 or current_offer < negotiation.final_offer:
            negotiation.final_offer = current_offer
        
        # Commit the negotiation
        db.session.commit()
        
        return jsonify({
            'response': bot_response,
            'current_offer': current_offer,
            'is_final': is_final,
            'negotiation_id': negotiation.id,
            'chat_history': negotiation.chat_history[-10:]  # Last 10 messages
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to process negotiation', 'message': str(e)}), 500

@vehicle_sales_bp.route('/<int:sale_id>/negotiations', methods=['GET'])
@jwt_required()
def get_sale_negotiations(sale_id):
    """Get negotiations for a vehicle sale (owner only)"""
    try:
        current_user_id = int(get_jwt_identity())
        
        vehicle_sale = VehicleSale.find_by_id(sale_id)
        if not vehicle_sale:
            return jsonify({'error': 'Vehicle sale not found'}), 404
        
        if vehicle_sale.user_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Get negotiations for this sale
        negotiations = Negotiation.get_sale_negotiations(sale_id)
        
        negotiations_data = []
        for negotiation in negotiations:
            neg_dict = negotiation.to_dict()
            # Only include negotiations with contact details (completed)
            if negotiation.buyer_name and negotiation.buyer_name != 'Anonymous':
                negotiations_data.append(neg_dict)
        
        return jsonify({
            'negotiations': negotiations_data,
            'count': len(negotiations_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get negotiations', 'message': str(e)}), 500

@vehicle_sales_bp.route('/negotiations/<int:negotiation_id>/accept', methods=['PUT'])
@jwt_required()
def accept_negotiation(negotiation_id):
    """Accept a negotiation offer"""
    try:
        current_user_id = int(get_jwt_identity())
        
        negotiation = Negotiation.find_by_id(negotiation_id)
        if not negotiation:
            return jsonify({'error': 'Negotiation not found'}), 404
        
        vehicle_sale = negotiation.vehicle_sale
        if vehicle_sale.user_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Accept the negotiation
        negotiation.update_status('accepted')
        vehicle_sale.mark_as_sold()
        
        return jsonify({
            'message': 'Negotiation accepted successfully',
            'negotiation': negotiation.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to accept negotiation', 'message': str(e)}), 500

@vehicle_sales_bp.route('/negotiations/<int:negotiation_id>/reject', methods=['PUT'])
@jwt_required()
def reject_negotiation(negotiation_id):
    """Reject a negotiation offer"""
    try:
        current_user_id = int(get_jwt_identity())
        
        negotiation = Negotiation.find_by_id(negotiation_id)
        if not negotiation:
            return jsonify({'error': 'Negotiation not found'}), 404
        
        vehicle_sale = negotiation.vehicle_sale
        if vehicle_sale.user_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Reject the negotiation
        negotiation.update_status('rejected')
        
        return jsonify({
            'message': 'Negotiation rejected',
            'negotiation': negotiation.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to reject negotiation', 'message': str(e)}), 500