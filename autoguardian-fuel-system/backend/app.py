"""
AutoGuardian Fuel Management System - Main Flask Application
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import datetime

# Import configuration
from config import config
from database import db

# Initialize extensions
cors = CORS()
jwt = JWTManager()

def create_app(config_name=None):
    """Application factory pattern"""
    
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    cors.init_app(app, origins=app.config['CORS_ORIGINS'])
    jwt.init_app(app)
    
    # Import models to ensure they're registered
    from models import user, vehicle, fuel_record, predictions, recommendations
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # JWT error handlers
    register_jwt_handlers(app)
    
    @app.route('/')
    def index():
        """Health check endpoint"""
        return jsonify({
            'message': 'AutoGuardian Fuel Management System API',
            'version': '1.0.0',
            'status': 'operational',
            'timestamp': datetime.utcnow().isoformat()
        })
    
    @app.route('/api/health')
    def health_check():
        """Detailed health check"""
        try:
            # Test database connection
            db.session.execute('SELECT 1')
            db_status = 'connected'
        except Exception as e:
            db_status = f'error: {str(e)}'
        
        return jsonify({
            'status': 'healthy',
            'database': db_status,
            'timestamp': datetime.utcnow().isoformat(),
            'environment': app.config['FLASK_ENV']
        })
    
    return app

def register_blueprints(app):
    """Register all route blueprints"""
    
    # Import route blueprints
    from routes.auth import auth_bp
    from routes.vehicles import vehicles_bp
    from routes.fuel_records import fuel_records_bp
    from routes.predictions import predictions_bp
    from routes.recommendations import recommendations_bp
    from routes.analytics import analytics_bp
    
    # Register blueprints with URL prefixes
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(vehicles_bp, url_prefix='/api/vehicles')
    app.register_blueprint(fuel_records_bp, url_prefix='/api/fuel-records')
    app.register_blueprint(predictions_bp, url_prefix='/api/predictions')
    app.register_blueprint(recommendations_bp, url_prefix='/api/recommendations')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')

def register_error_handlers(app):
    """Register error handlers"""
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad Request',
            'message': 'Invalid request data',
            'status_code': 400
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Authentication required',
            'status_code': 401
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'error': 'Forbidden',
            'message': 'Insufficient permissions',
            'status_code': 403
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'Resource not found',
            'status_code': 404
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'status_code': 500
        }), 500

def register_jwt_handlers(app):
    """Register JWT error handlers"""
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Token Expired',
            'message': 'The authentication token has expired',
            'status_code': 401
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'error': 'Invalid Token',
            'message': 'The authentication token is invalid',
            'status_code': 401
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'error': 'Authorization Required',
            'message': 'Authentication token is required',
            'status_code': 401
        }), 401
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Fresh Token Required',
            'message': 'A fresh authentication token is required',
            'status_code': 401
        }), 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Token Revoked',
            'message': 'The authentication token has been revoked',
            'status_code': 401
        }), 401

# Create application instance
app = create_app()

if __name__ == '__main__':
    # Development server
    port = int(os.environ.get('FLASK_PORT', 5000))
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"Starting AutoGuardian Fuel Management System")
    print(f"Server: http://{host}:{port}")
    print(f"Environment: {app.config['FLASK_ENV']}")
    print(f"Debug mode: {debug}")
    
    app.run(
        host=host,
        port=port,
        debug=debug
    )