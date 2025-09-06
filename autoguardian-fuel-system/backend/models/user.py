"""
AutoGuardian Fuel Management System - User Models
"""

from database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

class User(db.Model):
    """User model for authentication and profile management"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    vehicles = db.relationship('Vehicle', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    recommendations = db.relationship('AIRecommendation', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    preferences = db.relationship('UserPreferences', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def __init__(self, username, email, password, first_name=None, last_name=None, phone=None):
        """Initialize user with hashed password"""
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
    
    def set_password(self, password):
        """Set password with hashing"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        try:
            return check_password_hash(self.password_hash, password)
        except TypeError:
            # Fallback for older Werkzeug hashes - use bcrypt directly
            import bcrypt
            return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def generate_tokens(self):
        """Generate access and refresh tokens"""
        access_token = create_access_token(identity=str(self.id))
        refresh_token = create_refresh_token(identity=str(self.id))
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer'
        }
    
    @property
    def full_name(self):
        """Get user's full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.username
    
    @property
    def vehicle_count(self):
        """Get number of user's vehicles"""
        return self.vehicles.filter_by(is_active=True).count()
    
    def to_dict(self, include_sensitive=False):
        """Convert user to dictionary"""
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'phone': self.phone,
            'is_active': self.is_active,
            'vehicle_count': self.vehicle_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_sensitive:
            data['password_hash'] = self.password_hash
        
        return data
    
    @classmethod
    def find_by_username(cls, username):
        """Find user by username"""
        return cls.query.filter_by(username=username, is_active=True).first()
    
    @classmethod
    def find_by_email(cls, email):
        """Find user by email"""
        return cls.query.filter_by(email=email, is_active=True).first()
    
    @classmethod
    def find_by_id(cls, user_id):
        """Find user by ID"""
        return cls.query.filter_by(id=user_id, is_active=True).first()
    
    def __repr__(self):
        return f'<User {self.username}>'

class UserPreferences(db.Model):
    """User preferences for customization"""
    
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # Display preferences
    currency = db.Column(db.String(3), default='USD')
    distance_unit = db.Column(db.Enum('km', 'miles'), default='km')
    volume_unit = db.Column(db.Enum('liters', 'gallons'), default='liters')
    date_format = db.Column(db.String(20), default='YYYY-MM-DD')
    
    # Notification preferences
    notification_email = db.Column(db.Boolean, default=True)
    notification_maintenance = db.Column(db.Boolean, default=True)
    notification_efficiency = db.Column(db.Boolean, default=True)
    
    # System preferences
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, user_id, **kwargs):
        """Initialize user preferences"""
        self.user_id = user_id
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self):
        """Convert preferences to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'currency': self.currency,
            'distance_unit': self.distance_unit,
            'volume_unit': self.volume_unit,
            'date_format': self.date_format,
            'notification_email': self.notification_email,
            'notification_maintenance': self.notification_maintenance,
            'notification_efficiency': self.notification_efficiency,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def get_or_create(cls, user_id):
        """Get user preferences or create default ones"""
        preferences = cls.query.filter_by(user_id=user_id).first()
        if not preferences:
            preferences = cls(user_id=user_id)
            db.session.add(preferences)
            db.session.commit()
        return preferences
    
    def __repr__(self):
        return f'<UserPreferences user_id={self.user_id}>'