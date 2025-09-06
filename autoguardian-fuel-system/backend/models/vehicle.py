"""
AutoGuardian Fuel Management System - Vehicle Models
"""

from database import db
from datetime import datetime
from sqlalchemy import func

class Vehicle(db.Model):
    """Vehicle model for storing vehicle information"""
    
    __tablename__ = 'vehicles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicle_name = db.Column(db.String(100), nullable=False)
    
    # Vehicle specifications
    make = db.Column(db.String(50), nullable=False, index=True)
    model = db.Column(db.String(50), nullable=False, index=True)
    year = db.Column(db.Integer, nullable=False)
    vehicle_class = db.Column(db.String(50), nullable=False)
    engine_size = db.Column(db.Numeric(3, 1), nullable=False)
    cylinders = db.Column(db.Integer, nullable=False)
    transmission = db.Column(db.String(20), nullable=False)
    fuel_type = db.Column(db.String(20), nullable=False)
    
    # Tank and odometer info
    tank_capacity = db.Column(db.Numeric(5, 2), nullable=False)
    starting_odometer_value = db.Column(db.Integer, nullable=False, default=0)
    odo_meter_when_buy_vehicle = db.Column(db.Integer, nullable=False, default=0)
    full_tank_capacity = db.Column(db.Numeric(5, 2), nullable=False)
    initial_tank_percentage = db.Column(db.Numeric(5, 2), nullable=False, default=100.0)
    
    # Status and metadata
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    fuel_records = db.relationship('FuelRecord', backref='vehicle', lazy='dynamic', cascade='all, delete-orphan')
    ml_predictions = db.relationship('MLPrediction', backref='vehicle', lazy='dynamic', cascade='all, delete-orphan')
    ai_recommendations = db.relationship('AIRecommendation', backref='vehicle', lazy='dynamic', cascade='all, delete-orphan')
    statistics = db.relationship('VehicleStatistics', backref='vehicle', uselist=False, cascade='all, delete-orphan')
    
    def __init__(self, user_id, vehicle_name, make, model, year, 
                 vehicle_class, engine_size, cylinders, transmission, fuel_type,
                 tank_capacity, starting_odometer_value=0, odo_meter_when_buy_vehicle=None,
                 full_tank_capacity=None, initial_tank_percentage=100.0):
        """Initialize vehicle"""
        self.user_id = user_id
        self.vehicle_name = vehicle_name
        self.make = make.upper()
        self.model = model.upper()
        self.year = year
        self.vehicle_class = vehicle_class
        self.engine_size = engine_size
        self.cylinders = cylinders
        self.transmission = transmission
        self.fuel_type = fuel_type
        self.tank_capacity = tank_capacity
        self.starting_odometer_value = starting_odometer_value
        self.odo_meter_when_buy_vehicle = odo_meter_when_buy_vehicle or starting_odometer_value
        self.full_tank_capacity = full_tank_capacity or tank_capacity
        self.initial_tank_percentage = initial_tank_percentage
    
    @property
    def display_name(self):
        """Get vehicle display name"""
        return f"{self.year} {self.make} {self.model}"
    
    @property
    def engine_info(self):
        """Get engine information"""
        return f"{self.engine_size}L {self.cylinders} cylinders"
    
    @property
    def fuel_records_count(self):
        """Get number of fuel records"""
        return self.fuel_records.count()
    
    @property
    def latest_fuel_record(self):
        """Get latest fuel record"""
        return self.fuel_records.order_by(
            db.desc('record_date'), db.desc('record_time')
        ).first()
    
    @property
    def current_odometer(self):
        """Get current odometer reading from latest fuel record"""
        latest_record = self.latest_fuel_record
        return latest_record.odo_meter_current_value if latest_record else self.starting_odometer_value
    
    @property
    def total_distance_driven(self):
        """Get total distance driven"""
        return self.current_odometer - self.odo_meter_when_buy_vehicle
    
    @property
    def current_tank_percentage(self):
        """Get current tank percentage from latest fuel record or initial percentage"""
        latest_record = self.latest_fuel_record
        return latest_record.after_refuel_percentage if latest_record else self.initial_tank_percentage
    
    def get_ml_prediction_features(self):
        """Get features formatted for ML model prediction"""
        return {
            'MAKE': self.make,
            'MODEL': self.model,
            'VEHICLE CLASS': self.vehicle_class,
            'ENGINE SIZE': float(self.engine_size),
            'CYLINDERS': self.cylinders,
            'TRANSMISSION': self.transmission,
            'FUEL': self.fuel_type
        }
    
    def get_recent_consumption_data(self, days=30):
        """Get recent fuel consumption data"""
        from datetime import date, timedelta
        from .fuel_record import FuelRecord
        cutoff_date = date.today() - timedelta(days=days)
        
        return FuelRecord.query.filter(
            FuelRecord.vehicle_id == self.id,
            FuelRecord.record_date >= cutoff_date
        ).order_by(db.desc(FuelRecord.record_date)).all()
    
    def calculate_average_consumption(self, period_days=None):
        """Calculate average fuel consumption"""
        from .fuel_record import FuelRecord
        
        query = FuelRecord.query.filter(FuelRecord.vehicle_id == self.id)
        
        if period_days:
            from datetime import date, timedelta
            cutoff_date = date.today() - timedelta(days=period_days)
            query = query.filter(FuelRecord.record_date >= cutoff_date)
        
        records = query.filter(
            FuelRecord.actual_consumption_l_100km > 0
        ).all()
        
        if not records:
            return None
        
        total_fuel = sum(float(r.calculated_fuel_added) for r in records)
        total_km = sum(r.km_driven_since_last for r in records)
        
        return (total_fuel / total_km * 100) if total_km > 0 else None
    
    def get_consumption_by_driving_type(self):
        """Get consumption statistics by driving type"""
        from sqlalchemy import func
        
        results = db.session.query(
            FuelRecord.driving_type,
            func.count(FuelRecord.id).label('count'),
            func.sum(FuelRecord.calculated_fuel_added).label('total_fuel'),
            func.sum(FuelRecord.km_driven_since_last).label('total_km'),
            func.avg(FuelRecord.actual_consumption_l_100km).label('avg_consumption')
        ).filter(
            FuelRecord.vehicle_id == self.id,
            FuelRecord.actual_consumption_l_100km > 0
        ).group_by(FuelRecord.driving_type).all()
        
        return {
            result.driving_type: {
                'count': result.count,
                'total_fuel': float(result.total_fuel or 0),
                'total_km': result.total_km or 0,
                'avg_consumption': float(result.avg_consumption or 0)
            }
            for result in results
        }
    
    def to_dict(self, include_stats=True):
        """Convert vehicle to dictionary"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'vehicle_name': self.vehicle_name,
            'display_name': self.display_name,
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'vehicle_class': self.vehicle_class,
            'engine_size': float(self.engine_size),
            'engine_info': self.engine_info,
            'cylinders': self.cylinders,
            'transmission': self.transmission,
            'fuel_type': self.fuel_type,
            'tank_capacity': float(self.tank_capacity),
            'full_tank_capacity': float(self.full_tank_capacity),
            'starting_odometer_value': self.starting_odometer_value,
            'odo_meter_when_buy_vehicle': self.odo_meter_when_buy_vehicle,
            'initial_tank_percentage': float(self.initial_tank_percentage),
            'current_odometer': self.current_odometer,
            'total_distance_driven': self.total_distance_driven,
            'fuel_records_count': self.fuel_records_count,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_stats:
            latest_record = self.latest_fuel_record
            data['latest_fuel_record'] = latest_record.to_dict() if latest_record else None
            data['average_consumption_30d'] = self.calculate_average_consumption(30)
            data['consumption_by_type'] = self.get_consumption_by_driving_type()
        
        return data
    
    @classmethod
    def find_by_id(cls, vehicle_id):
        """Find vehicle by id"""
        return cls.query.filter_by(id=vehicle_id, is_active=True).first()
    
    @classmethod
    def find_by_user(cls, user_id):
        """Find all vehicles for a user"""
        return cls.query.filter_by(user_id=user_id, is_active=True).all()
    
    def __repr__(self):
        return f'<Vehicle {self.id}: {self.display_name}>'

class VehicleStatistics(db.Model):
    """Vehicle statistics for caching performance metrics"""
    
    __tablename__ = 'vehicle_statistics'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), 
                          nullable=False, unique=True)
    
    # Cached statistics
    total_fuel_consumed = db.Column(db.Numeric(10, 2), default=0)
    total_distance_driven = db.Column(db.Integer, default=0)
    total_cost = db.Column(db.Numeric(10, 2), default=0)
    average_consumption = db.Column(db.Numeric(6, 2), default=0)
    last_fuel_record_date = db.Column(db.Date)
    total_refuels = db.Column(db.Integer, default=0)
    efficiency_trend = db.Column(db.String(20), default='stable')  # improving, stable, declining
    
    # Metadata
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, vehicle_id):
        """Initialize vehicle statistics"""
        self.vehicle_id = vehicle_id
        self.refresh_statistics()
    
    def refresh_statistics(self):
        """Refresh cached statistics from fuel records"""
        from sqlalchemy import func
        
        # Get aggregated data from fuel records
        result = db.session.query(
            func.count(FuelRecord.id).label('total_refuels'),
            func.sum(FuelRecord.calculated_fuel_added).label('total_fuel'),
            func.sum(FuelRecord.total_cost).label('total_cost'),
            func.sum(FuelRecord.km_driven_since_last).label('total_distance'),
            func.max(FuelRecord.record_date).label('last_record_date')
        ).filter(FuelRecord.vehicle_id == self.vehicle_id).first()
        
        if result and result.total_refuels > 0:
            self.total_refuels = result.total_refuels
            self.total_fuel_consumed = result.total_fuel or 0
            self.total_cost = result.total_cost or 0
            self.total_distance_driven = result.total_distance or 0
            self.last_fuel_record_date = result.last_record_date
            
            # Calculate average consumption
            if self.total_distance_driven > 0:
                self.average_consumption = (float(self.total_fuel_consumed) / self.total_distance_driven) * 100
            
            # Determine efficiency trend (simplified logic)
            recent_records = db.session.query(FuelRecord.actual_consumption_l_100km).filter(
                FuelRecord.vehicle_id == self.vehicle_id,
                FuelRecord.actual_consumption_l_100km > 0
            ).order_by(db.desc(FuelRecord.record_date)).limit(5).all()
            
            if len(recent_records) >= 3:
                recent_avg = sum(float(r.actual_consumption_l_100km) for r in recent_records[:3]) / 3
                older_avg = sum(float(r.actual_consumption_l_100km) for r in recent_records[-3:]) / 3
                
                if recent_avg < older_avg * 0.95:
                    self.efficiency_trend = 'improving'
                elif recent_avg > older_avg * 1.05:
                    self.efficiency_trend = 'declining'
                else:
                    self.efficiency_trend = 'stable'
        
        self.last_updated = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        """Convert statistics to dictionary"""
        return {
            'vehicle_id': self.vehicle_id,
            'total_fuel_consumed': float(self.total_fuel_consumed),
            'total_distance_driven': self.total_distance_driven,
            'total_cost': float(self.total_cost),
            'average_consumption': float(self.average_consumption),
            'last_fuel_record_date': self.last_fuel_record_date.isoformat() if self.last_fuel_record_date else None,
            'total_refuels': self.total_refuels,
            'efficiency_trend': self.efficiency_trend,
            'cost_per_km': float(self.total_cost / self.total_distance_driven) if self.total_distance_driven > 0 else 0,
            'last_updated': self.last_updated.isoformat()
        }
    
    @classmethod
    def get_or_create(cls, vehicle_id):
        """Get vehicle statistics or create if not exists"""
        stats = cls.query.filter_by(vehicle_id=vehicle_id).first()
        if not stats:
            stats = cls(vehicle_id=vehicle_id)
            db.session.add(stats)
            db.session.commit()
        return stats
    
    def __repr__(self):
        return f'<VehicleStatistics {self.vehicle_id}>'

# Import FuelRecord here to avoid circular import
from .fuel_record import FuelRecord