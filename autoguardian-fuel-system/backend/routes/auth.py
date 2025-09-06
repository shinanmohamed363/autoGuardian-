"""
AutoGuardian Fuel Management System - Authentication Routes
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, 
    get_jwt_identity, get_jwt
)
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
import re

from utils.validators import validate_email, validate_password, validate_required_fields
from database import db
from models.user import User, UserPreferences

# Create authentication blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Invalid JSON data',
                'message': 'Request body must contain valid JSON'
            }), 400
        
        # Validate required fields
        required_fields = ['username', 'email', 'password']
        missing_fields = validate_required_fields(data, required_fields)
        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing_fields
            }), 400
        
        username = data['username'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        phone = data.get('phone', '').strip()
        
        # Validate input data
        validation_errors = []
        
        # Username validation
        if len(username) < 3 or len(username) > 50:
            validation_errors.append("Username must be between 3 and 50 characters")
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            validation_errors.append("Username can only contain letters, numbers, and underscores")
        
        # Email validation
        if not validate_email(email):
            validation_errors.append("Invalid email format")
        
        # Password validation
        password_errors = validate_password(password)
        validation_errors.extend(password_errors)
        
        if validation_errors:
            return jsonify({
                'error': 'Validation failed',
                'validation_errors': validation_errors
            }), 400
        
        # Check if user already exists
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            if existing_user.username == username:
                return jsonify({
                    'error': 'Username already exists',
                    'message': 'Please choose a different username'
                }), 409
            else:
                return jsonify({
                    'error': 'Email already registered',
                    'message': 'Please use a different email or try logging in'
                }), 409
        
        # Create new user
        user = User(
            username=username,
            email=email,
            password=password,
            first_name=first_name if first_name else None,
            last_name=last_name if last_name else None,
            phone=phone if phone else None
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Create default user preferences
        preferences = UserPreferences(user_id=user.id)
        db.session.add(preferences)
        db.session.commit()
        
        # Generate tokens
        tokens = user.generate_tokens()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'tokens': tokens
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Registration failed',
            'message': str(e)
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return tokens"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Invalid JSON data',
                'message': 'Request body must contain valid JSON'
            }), 400
        
        # Validate required fields
        required_fields = ['username', 'password']
        missing_fields = validate_required_fields(data, required_fields)
        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing_fields
            }), 400
        
        username_or_email = data['username'].strip()
        password = data['password']
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == username_or_email) | 
            (User.email == username_or_email.lower())
        ).first()
        
        if not user or not user.is_active:
            return jsonify({
                'error': 'Invalid credentials',
                'message': 'Username/email or password is incorrect'
            }), 401
        
        if not user.check_password(password):
            return jsonify({
                'error': 'Invalid credentials',
                'message': 'Username/email or password is incorrect'
            }), 401
        
        # Generate tokens
        tokens = user.generate_tokens()
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'tokens': tokens
        }), 200
        
    except Exception as e:
        print(f"LOGIN ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Login failed',
            'message': str(e)
        }), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token using refresh token"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'error': 'User not found',
                'message': 'Invalid refresh token'
            }), 401
        
        # Generate new access token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'access_token': access_token,
            'token_type': 'Bearer'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Token refresh failed',
            'message': str(e)
        }), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'error': 'User not found',
                'message': 'Invalid access token'
            }), 401
        
        # Get user preferences
        preferences = UserPreferences.get_or_create(user.id)
        
        profile_data = user.to_dict()
        profile_data['preferences'] = preferences.to_dict()
        
        return jsonify({
            'user': profile_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to get profile',
            'message': str(e)
        }), 500

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update current user profile"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'error': 'User not found',
                'message': 'Invalid access token'
            }), 401
        
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Invalid JSON data',
                'message': 'Request body must contain valid JSON'
            }), 400
        
        # Update allowed fields
        updatable_fields = ['first_name', 'last_name', 'phone']
        updated_fields = []
        
        for field in updatable_fields:
            if field in data:
                setattr(user, field, data[field].strip() if data[field] else None)
                updated_fields.append(field)
        
        # Update email if provided (with validation)
        if 'email' in data:
            new_email = data['email'].strip().lower()
            if not validate_email(new_email):
                return jsonify({
                    'error': 'Invalid email format',
                    'message': 'Please provide a valid email address'
                }), 400
            
            # Check if email is already taken by another user
            existing_user = User.query.filter(
                User.email == new_email,
                User.id != user.id
            ).first()
            
            if existing_user:
                return jsonify({
                    'error': 'Email already exists',
                    'message': 'This email is already registered to another user'
                }), 409
            
            user.email = new_email
            updated_fields.append('email')
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'updated_fields': updated_fields,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Profile update failed',
            'message': str(e)
        }), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'error': 'User not found',
                'message': 'Invalid access token'
            }), 401
        
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Invalid JSON data',
                'message': 'Request body must contain valid JSON'
            }), 400
        
        # Validate required fields
        required_fields = ['current_password', 'new_password']
        missing_fields = validate_required_fields(data, required_fields)
        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing_fields
            }), 400
        
        current_password = data['current_password']
        new_password = data['new_password']
        
        # Verify current password
        if not user.check_password(current_password):
            return jsonify({
                'error': 'Invalid current password',
                'message': 'Current password is incorrect'
            }), 401
        
        # Validate new password
        password_errors = validate_password(new_password)
        if password_errors:
            return jsonify({
                'error': 'Invalid new password',
                'validation_errors': password_errors
            }), 400
        
        # Check if new password is different from current
        if current_password == new_password:
            return jsonify({
                'error': 'Same password',
                'message': 'New password must be different from current password'
            }), 400
        
        # Update password
        user.set_password(new_password)
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Password changed successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Password change failed',
            'message': str(e)
        }), 500

@auth_bp.route('/preferences', methods=['GET'])
@jwt_required()
def get_preferences():
    """Get user preferences"""
    try:
        current_user_id = int(get_jwt_identity())
        preferences = UserPreferences.get_or_create(current_user_id)
        
        return jsonify({
            'preferences': preferences.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to get preferences',
            'message': str(e)
        }), 500

@auth_bp.route('/preferences', methods=['PUT'])
@jwt_required()
def update_preferences():
    """Update user preferences"""
    try:
        current_user_id = int(get_jwt_identity())
        preferences = UserPreferences.get_or_create(current_user_id)
        
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Invalid JSON data',
                'message': 'Request body must contain valid JSON'
            }), 400
        
        # Update allowed fields
        updatable_fields = [
            'currency', 'distance_unit', 'volume_unit', 'date_format',
            'notification_email', 'notification_maintenance', 'notification_efficiency'
        ]
        
        updated_fields = []
        for field in updatable_fields:
            if field in data:
                setattr(preferences, field, data[field])
                updated_fields.append(field)
        
        preferences.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Preferences updated successfully',
            'updated_fields': updated_fields,
            'preferences': preferences.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Preferences update failed',
            'message': str(e)
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user (token blacklisting would be implemented here in production)"""
    try:
        # In a production system, you would add the token to a blacklist
        # For now, we just return success and let the client handle token removal
        
        return jsonify({
            'message': 'Logged out successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Logout failed',
            'message': str(e)
        }), 500

@auth_bp.route('/verify', methods=['GET'])
@jwt_required()
def verify_token():
    """Verify token validity"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'valid': False,
                'message': 'User not found'
            }), 401
        
        jwt_data = get_jwt()
        
        return jsonify({
            'valid': True,
            'user': user.to_dict(),
            'token_info': {
                'user_id': current_user_id,
                'expires_at': jwt_data.get('exp'),
                'issued_at': jwt_data.get('iat')
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'valid': False,
            'error': str(e)
        }), 401