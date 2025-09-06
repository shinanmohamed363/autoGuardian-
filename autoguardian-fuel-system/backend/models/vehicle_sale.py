"""
AutoGuardian Fuel Management System - Vehicle Sale Model
"""

from datetime import datetime, timezone
from database import db
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

class VehicleSale(db.Model):
    """Model for vehicles listed for sale"""
    __tablename__ = 'vehicle_sales'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    selling_price = Column(Float, nullable=False)  # Asking price
    minimum_price = Column(Float, nullable=False)  # Minimum acceptable price
    features = Column(JSON, nullable=True)  # Array of additional features/improvements
    description = Column(Text, nullable=True)  # Additional description
    is_active = Column(Boolean, default=True)  # Whether the sale is still active
    is_sold = Column(Boolean, default=False)  # Whether the vehicle has been sold
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    user = relationship("User", backref="vehicle_sales")
    vehicle = relationship("Vehicle", backref="sale_listings")
    negotiations = relationship("Negotiation", back_populates="vehicle_sale", cascade="all, delete-orphan")
    
    def __init__(self, user_id, vehicle_id, selling_price, minimum_price, features=None, description=None):
        self.user_id = user_id
        self.vehicle_id = vehicle_id
        self.selling_price = selling_price
        self.minimum_price = minimum_price
        self.features = features or []
        self.description = description
    
    def to_dict(self, include_sensitive=False):
        """Convert vehicle sale to dictionary"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'vehicle_id': self.vehicle_id,
            'selling_price': self.selling_price,
            'features': self.features,
            'description': self.description,
            'is_active': self.is_active,
            'is_sold': self.is_sold,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        
        # Only include minimum price for owner or in negotiations
        if include_sensitive:
            data['minimum_price'] = self.minimum_price
            
        # Include vehicle details if available
        if hasattr(self, 'vehicle') and self.vehicle:
            data['vehicle'] = {
                'vehicle_name': self.vehicle.vehicle_name,
                'make': self.vehicle.make,
                'model': self.vehicle.model,
                'year': self.vehicle.year,
                'vehicle_class': self.vehicle.vehicle_class,
                'engine_size': self.vehicle.engine_size,
                'fuel_type': self.vehicle.fuel_type,
                'transmission': self.vehicle.transmission,
                'current_odometer': self.vehicle.current_odometer
            }
        
        return data
    
    @classmethod
    def get_active_sales(cls, exclude_user_id=None):
        """Get all active vehicle sales"""
        query = cls.query.filter_by(is_active=True, is_sold=False)
        if exclude_user_id:
            query = query.filter(cls.user_id != exclude_user_id)
        return query.all()
    
    @classmethod
    def get_user_sales(cls, user_id):
        """Get all sales by a specific user"""
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def find_by_id(cls, sale_id):
        """Find sale by ID"""
        return cls.query.get(sale_id)
    
    def update_sale(self, **kwargs):
        """Update sale details"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()
    
    def deactivate_sale(self):
        """Deactivate the sale"""
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()
    
    def mark_as_sold(self):
        """Mark the vehicle as sold"""
        self.is_sold = True
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()


class Negotiation(db.Model):
    """Model for negotiations on vehicle sales"""
    __tablename__ = 'negotiations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_sale_id = Column(Integer, ForeignKey('vehicle_sales.id'), nullable=False)
    buyer_name = Column(String(100), nullable=False)
    buyer_email = Column(String(150), nullable=False)
    buyer_contact = Column(String(20), nullable=True)
    final_offer = Column(Float, nullable=False)  # Final negotiated price
    chat_history = Column(JSON, nullable=True)  # Complete chat conversation
    status = Column(String(20), default='pending')  # pending, accepted, rejected
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    vehicle_sale = relationship("VehicleSale", back_populates="negotiations")
    
    def __init__(self, vehicle_sale_id, buyer_name, buyer_email, final_offer, buyer_contact=None, chat_history=None):
        self.vehicle_sale_id = vehicle_sale_id
        self.buyer_name = buyer_name
        self.buyer_email = buyer_email
        self.buyer_contact = buyer_contact
        self.final_offer = final_offer
        self.chat_history = chat_history or []
    
    def to_dict(self):
        """Convert negotiation to dictionary"""
        return {
            'id': self.id,
            'vehicle_sale_id': self.vehicle_sale_id,
            'buyer_name': self.buyer_name,
            'buyer_email': self.buyer_email,
            'buyer_contact': self.buyer_contact,
            'final_offer': self.final_offer,
            'chat_history': self.chat_history,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    @classmethod
    def get_sale_negotiations(cls, vehicle_sale_id):
        """Get all negotiations for a specific sale"""
        return cls.query.filter_by(vehicle_sale_id=vehicle_sale_id).all()
    
    @classmethod
    def find_by_id(cls, negotiation_id):
        """Find negotiation by ID"""
        return cls.query.get(negotiation_id)
    
    def update_status(self, status):
        """Update negotiation status"""
        self.status = status
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()
    
    def add_chat_message(self, sender, message):
        """Add a message to the chat history"""
        if not self.chat_history:
            self.chat_history = []
        
        chat_message = {
            'sender': sender,  # 'buyer' or 'system'
            'message': message,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        self.chat_history.append(chat_message)
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()