"""
AutoGuardian Fuel Management System - AI Recommendation Models
"""

from database import db
from datetime import datetime
from enum import Enum

class RecommendationType(Enum):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    MAINTENANCE = 'maintenance'
    EFFICIENCY = 'efficiency'

class PriorityLevel(Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICAL = 'critical'

class AIRecommendation(db.Model):
    """AI recommendation model for storing intelligent suggestions"""
    
    __tablename__ = 'ai_recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    
    # Recommendation content
    recommendation_type = db.Column(db.String(20), nullable=False, index=True)
    recommendation_title = db.Column(db.String(200), nullable=False)
    recommendation_text = db.Column(db.Text, nullable=False)
    performance_analysis = db.Column(db.Text)
    
    # Metadata
    priority_level = db.Column(db.String(20), default='medium', index=True)
    category = db.Column(db.String(50))  # fuel_efficiency, cost_saving, maintenance, environmental
    impact_score = db.Column(db.Numeric(3, 2))  # 0.00 to 10.00 potential impact score
    
    # Status tracking
    is_read = db.Column(db.Boolean, default=False, index=True)
    is_implemented = db.Column(db.Boolean, default=False)
    implementation_notes = db.Column(db.Text)
    
    # AI generation metadata
    ai_model_used = db.Column(db.String(50), default='gemini-2.0-flash')
    generation_prompt = db.Column(db.Text)
    confidence_level = db.Column(db.Numeric(3, 2))  # AI confidence in recommendation
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    read_at = db.Column(db.DateTime)
    implemented_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)  # For time-sensitive recommendations
    
    def __init__(self, user_id, vehicle_id, recommendation_type, recommendation_title,
                 recommendation_text, performance_analysis=None, priority_level='medium',
                 category=None, impact_score=None, ai_model_used='gemini-2.0-flash',
                 confidence_level=None, expires_at=None):
        """Initialize AI recommendation"""
        self.user_id = user_id
        self.vehicle_id = vehicle_id
        # Validate recommendation type
        valid_types = ['daily', 'weekly', 'monthly', 'maintenance', 'efficiency']
        if recommendation_type not in valid_types:
            raise ValueError(f"Invalid recommendation_type: {recommendation_type}. Must be one of: {valid_types}")
        self.recommendation_type = recommendation_type
        self.recommendation_title = recommendation_title
        self.recommendation_text = recommendation_text
        self.performance_analysis = performance_analysis
        # Validate priority level
        valid_priorities = ['low', 'medium', 'high', 'critical']
        if priority_level not in valid_priorities:
            raise ValueError(f"Invalid priority_level: {priority_level}. Must be one of: {valid_priorities}")
        self.priority_level = priority_level
        self.category = category
        self.impact_score = impact_score
        self.ai_model_used = ai_model_used
        self.confidence_level = confidence_level
        self.expires_at = expires_at
    
    @property
    def is_expired(self):
        """Check if recommendation is expired"""
        return self.expires_at and datetime.utcnow() > self.expires_at
    
    @property
    def age_in_days(self):
        """Get age of recommendation in days"""
        return (datetime.utcnow() - self.created_at).days
    
    @property
    def priority_color(self):
        """Get color code for priority level"""
        colors = {
            'low': '#28a745',      # Green
            'medium': '#ffc107',   # Yellow
            'high': '#fd7e14',     # Orange
            'critical': '#dc3545'  # Red
        }
        return colors.get(self.priority_level, '#6c757d')
    
    @property
    def category_icon(self):
        """Get icon for recommendation category"""
        icons = {
            'fuel_efficiency': '⛽',
            'cost_saving': '💰',
            'maintenance': '🔧',
            'environmental': '🌱',
            'driving_behavior': '🚗',
            'route_optimization': '🗺️'
        }
        return icons.get(self.category, '📋')
    
    def mark_as_read(self):
        """Mark recommendation as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = datetime.utcnow()
            db.session.commit()
    
    def mark_as_implemented(self, implementation_notes=None):
        """Mark recommendation as implemented"""
        self.is_implemented = True
        self.implemented_at = datetime.utcnow()
        if implementation_notes:
            self.implementation_notes = implementation_notes
        db.session.commit()
    
    def calculate_potential_savings(self):
        """Calculate potential savings from implementing recommendation"""
        # This would be enhanced based on recommendation type and vehicle data
        base_savings = {
            'fuel_efficiency': 0.15,  # 15% fuel savings
            'cost_saving': 0.10,      # 10% cost savings
            'maintenance': 0.05,      # 5% maintenance cost reduction
            'environmental': 0.12     # 12% emissions reduction
        }
        
        savings_factor = base_savings.get(self.category, 0.08)
        
        # Get vehicle statistics for calculation
        from .vehicle import VehicleStatistics
        stats = VehicleStatistics.query.filter_by(vehicle_id=self.vehicle_id).first()
        
        if stats and stats.total_cost > 0:
            monthly_cost = float(stats.total_cost) / max(1, stats.total_refuels)  # Rough monthly estimate
            potential_monthly_savings = monthly_cost * savings_factor
            potential_yearly_savings = potential_monthly_savings * 12
            
            return {
                'monthly_savings': round(potential_monthly_savings, 2),
                'yearly_savings': round(potential_yearly_savings, 2),
                'savings_percentage': round(savings_factor * 100, 1)
            }
        
        return None
    
    def generate_summary(self):
        """Generate a brief summary of the recommendation"""
        # Extract first sentence or first 100 characters
        first_sentence = self.recommendation_text.split('.')[0]
        if len(first_sentence) > 100:
            return first_sentence[:100] + '...'
        return first_sentence + '.'
    
    def to_dict(self, include_full_text=True):
        """Convert recommendation to dictionary"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'vehicle_id': self.vehicle_id,
            'recommendation_type': self.recommendation_type,
            'recommendation_title': self.recommendation_title,
            'priority_level': self.priority_level,
            'priority_color': self.priority_color,
            'category': self.category,
            'category_icon': self.category_icon,
            'impact_score': float(self.impact_score) if self.impact_score else None,
            'is_read': self.is_read,
            'is_implemented': self.is_implemented,
            'is_expired': self.is_expired,
            'age_in_days': self.age_in_days,
            'ai_model_used': self.ai_model_used,
            'confidence_level': float(self.confidence_level) if self.confidence_level else None,
            'created_at': self.created_at.isoformat(),
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'implemented_at': self.implemented_at.isoformat() if self.implemented_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        }
        
        if include_full_text:
            data['recommendation_text'] = self.recommendation_text
            data['performance_analysis'] = self.performance_analysis
            data['implementation_notes'] = self.implementation_notes
            data['potential_savings'] = self.calculate_potential_savings()
        else:
            data['summary'] = self.generate_summary()
        
        return data
    
    @classmethod
    def get_user_recommendations(cls, user_id, limit=20, unread_only=False, priority_filter=None):
        """Get recommendations for a user"""
        query = cls.query.filter_by(user_id=user_id)
        
        if unread_only:
            query = query.filter_by(is_read=False)
        
        if priority_filter:
            query = query.filter_by(priority_level=priority_filter)
        
        return query.order_by(
            cls.priority_level.desc(),
            db.desc(cls.created_at)
        ).limit(limit).all()
    
    @classmethod
    def get_vehicle_recommendations(cls, vehicle_id, limit=10):
        """Get recommendations for a specific vehicle"""
        return cls.query.filter_by(vehicle_id=vehicle_id).order_by(
            cls.priority_level.desc(),
            db.desc(cls.created_at)
        ).limit(limit).all()
    
    @classmethod
    def get_by_type(cls, user_id, recommendation_type, limit=5):
        """Get recommendations by type"""
        return cls.query.filter(
            cls.user_id == user_id,
            cls.recommendation_type == recommendation_type
        ).order_by(db.desc(cls.created_at)).limit(limit).all()
    
    @classmethod
    def create_fuel_efficiency_recommendation(cls, user_id, vehicle_id, analysis_data):
        """Create a fuel efficiency recommendation"""
        title = "Improve Fuel Efficiency"
        text = cls._generate_efficiency_text(analysis_data)
        
        return cls(
            user_id=user_id,
            vehicle_id=vehicle_id,
            recommendation_type='efficiency',
            recommendation_title=title,
            recommendation_text=text,
            category='fuel_efficiency',
            priority_level='medium',
            impact_score=7.5
        )
    
    @classmethod
    def create_maintenance_recommendation(cls, user_id, vehicle_id, maintenance_data):
        """Create a maintenance recommendation"""
        title = "Vehicle Maintenance Required"
        text = cls._generate_maintenance_text(maintenance_data)
        
        return cls(
            user_id=user_id,
            vehicle_id=vehicle_id,
            recommendation_type='maintenance',
            recommendation_title=title,
            recommendation_text=text,
            category='maintenance',
            priority_level='high',
            impact_score=8.0
        )
    
    @classmethod
    def _generate_efficiency_text(cls, analysis_data):
        """Generate efficiency recommendation text"""
        # This would be replaced with AI-generated content
        base_text = "Based on your recent fuel consumption patterns, here are some recommendations to improve efficiency: "
        suggestions = [
            "Maintain steady speeds on highways",
            "Avoid rapid acceleration and hard braking",
            "Keep tires properly inflated",
            "Remove excess weight from your vehicle",
            "Use air conditioning wisely"
        ]
        return base_text + "; ".join(suggestions) + "."
    
    @classmethod
    def _generate_maintenance_text(cls, maintenance_data):
        """Generate maintenance recommendation text"""
        # This would be replaced with AI-generated content
        return "Your vehicle's fuel consumption has increased recently, which may indicate maintenance issues. Consider checking your air filter, spark plugs, and tire pressure. Schedule a routine maintenance check to ensure optimal performance."
    
    def __repr__(self):
        return f'<AIRecommendation {self.id}: {self.recommendation_type.value} for {self.vehicle_id}>'