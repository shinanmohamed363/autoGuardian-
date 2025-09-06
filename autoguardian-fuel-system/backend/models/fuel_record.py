"""
AutoGuardian Fuel Management System - Fuel Record Models
"""

from database import db
from datetime import datetime, date, time, timedelta

class FuelRecord(db.Model):
    """Fuel record model for tracking refueling events"""
    
    __tablename__ = 'fuel_records'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    
    # Date and time information
    record_date = db.Column(db.Date, nullable=False, index=True)
    record_time = db.Column(db.Time, nullable=False)
    
    # Fuel tank information
    existing_tank_percentage = db.Column(db.Numeric(5, 2), nullable=False)
    after_refuel_percentage = db.Column(db.Numeric(5, 2), nullable=False)
    
    # Odometer and driving information
    odo_meter_current_value = db.Column(db.Integer, nullable=False)
    driving_type = db.Column(db.Enum('city', 'highway', 'mix'), nullable=False, index=True)
    location = db.Column(db.String(100), nullable=False, index=True)
    
    # Cost information
    fuel_price = db.Column(db.Numeric(6, 2), nullable=False)  # Price per liter in cents
    
    # Calculated fields (computed automatically)
    calculated_fuel_added = db.Column(db.Numeric(6, 2), default=0)
    total_cost = db.Column(db.Numeric(8, 2), default=0)
    km_driven_since_last = db.Column(db.Integer, default=0)
    actual_consumption_l_100km = db.Column(db.Numeric(6, 2), default=0)
    
    # Additional information
    notes = db.Column(db.Text)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, vehicle_id, record_date, record_time, existing_tank_percentage,
                 after_refuel_percentage, odo_meter_current_value, driving_type,
                 location, fuel_price, notes=None):
        """Initialize fuel record"""
        self.vehicle_id = vehicle_id
        self.record_date = record_date if isinstance(record_date, date) else datetime.strptime(record_date, '%Y-%m-%d').date()
        self.record_time = record_time if isinstance(record_time, time) else datetime.strptime(record_time, '%H:%M').time()
        self.existing_tank_percentage = existing_tank_percentage
        self.after_refuel_percentage = after_refuel_percentage
        self.odo_meter_current_value = odo_meter_current_value
        self.driving_type = driving_type
        self.location = location
        self.fuel_price = fuel_price
        self.notes = notes
        
        # Calculate derived fields
        self._calculate_fuel_metrics()
    
    def _calculate_fuel_metrics(self):
        """Calculate fuel-related metrics"""
        from .vehicle import Vehicle
        
        # Get vehicle to access tank capacity
        vehicle = Vehicle.find_by_id(self.vehicle_id)
        if not vehicle:
            return
        
        # Calculate fuel added
        fuel_percentage_added = float(self.after_refuel_percentage) - float(self.existing_tank_percentage)
        self.calculated_fuel_added = (fuel_percentage_added / 100) * float(vehicle.full_tank_capacity)
        
        # Calculate total cost (fuel_price is in cents per liter)
        self.total_cost = self.calculated_fuel_added * float(self.fuel_price) / 100
        
        # Calculate km driven and consumption
        previous_record = self.get_previous_record()
        if previous_record:
            self.km_driven_since_last = self.odo_meter_current_value - previous_record.odo_meter_current_value
            # For subsequent records, calculate fuel consumption based on tank depletion since last refuel
            fuel_consumed = ((float(previous_record.after_refuel_percentage) - float(self.existing_tank_percentage)) / 100) * float(vehicle.full_tank_capacity)
            if self.km_driven_since_last > 0 and fuel_consumed > 0:
                self.actual_consumption_l_100km = (fuel_consumed / self.km_driven_since_last) * 100
            else:
                self.actual_consumption_l_100km = 0
        else:
            # First record - use starting odometer and initial tank percentage
            self.km_driven_since_last = self.odo_meter_current_value - vehicle.starting_odometer_value
            # For first record, calculate fuel consumption based on initial tank vs existing tank
            fuel_consumed = ((float(vehicle.initial_tank_percentage) - float(self.existing_tank_percentage)) / 100) * float(vehicle.full_tank_capacity)
            if self.km_driven_since_last > 0 and fuel_consumed > 0:
                self.actual_consumption_l_100km = (fuel_consumed / self.km_driven_since_last) * 100
            else:
                self.actual_consumption_l_100km = 0
    
    def get_previous_record(self):
        """Get the previous fuel record for this vehicle"""
        return FuelRecord.query.filter(
            FuelRecord.vehicle_id == self.vehicle_id,
            db.or_(
                FuelRecord.record_date < self.record_date,
                db.and_(
                    FuelRecord.record_date == self.record_date,
                    FuelRecord.record_time < self.record_time
                )
            )
        ).order_by(
            db.desc(FuelRecord.record_date),
            db.desc(FuelRecord.record_time)
        ).first()
    
    def get_next_record(self):
        """Get the next fuel record for this vehicle"""
        return FuelRecord.query.filter(
            FuelRecord.vehicle_id == self.vehicle_id,
            db.or_(
                FuelRecord.record_date > self.record_date,
                db.and_(
                    FuelRecord.record_date == self.record_date,
                    FuelRecord.record_time > self.record_time
                )
            )
        ).order_by(
            FuelRecord.record_date,
            FuelRecord.record_time
        ).first()
    
    @property
    def datetime(self):
        """Get combined datetime"""
        return datetime.combine(self.record_date, self.record_time)
    
    @property
    def fuel_efficiency_rating(self):
        """Get efficiency rating based on consumption"""
        consumption = float(self.actual_consumption_l_100km)
        if consumption == 0:
            return 'N/A'
        elif consumption < 6:
            return 'Excellent'
        elif consumption < 8:
            return 'Good'
        elif consumption < 10:
            return 'Average'
        elif consumption < 12:
            return 'Below Average'
        else:
            return 'Poor'
    
    @property
    def cost_per_km(self):
        """Calculate cost per kilometer"""
        return float(self.total_cost / self.km_driven_since_last) if self.km_driven_since_last > 0 else 0
    
    @property
    def fuel_price_per_liter(self):
        """Get fuel price per liter (converted from cents)"""
        return float(self.fuel_price) / 100
    
    def validate_odometer(self):
        """Validate odometer reading against previous records"""
        previous_record = self.get_previous_record()
        if previous_record and self.odo_meter_current_value < previous_record.odo_meter_current_value:
            return False, f"Odometer reading ({self.odo_meter_current_value}) cannot be less than previous reading ({previous_record.odo_meter_current_value})"
        return True, None
    
    def validate_tank_percentages(self):
        """Validate tank percentage values"""
        if not (0 <= self.existing_tank_percentage <= 100):
            return False, "Existing tank percentage must be between 0 and 100"
        if not (0 <= self.after_refuel_percentage <= 100):
            return False, "After refuel percentage must be between 0 and 100"
        if self.after_refuel_percentage <= self.existing_tank_percentage:
            return False, "After refuel percentage must be greater than existing percentage"
        return True, None
    
    def recalculate_metrics(self):
        """Recalculate all derived metrics"""
        self._calculate_fuel_metrics()
        
        # Update next record's km_driven_since_last if it exists
        next_record = self.get_next_record()
        if next_record:
            next_record.km_driven_since_last = next_record.odo_meter_current_value - self.odo_meter_current_value
            if next_record.km_driven_since_last > 0:
                next_record.actual_consumption_l_100km = (next_record.calculated_fuel_added / next_record.km_driven_since_last) * 100
            else:
                next_record.actual_consumption_l_100km = 0
    
    def to_dict(self, include_analysis=False):
        """Convert fuel record to dictionary"""
        data = {
            'id': self.id,
            'vehicle_id': self.vehicle_id,
            'record_date': self.record_date.isoformat(),
            'record_time': self.record_time.strftime('%H:%M'),
            'datetime': self.datetime.isoformat(),
            'existing_tank_percentage': float(self.existing_tank_percentage),
            'after_refuel_percentage': float(self.after_refuel_percentage),
            'fuel_percentage_added': float(self.after_refuel_percentage - self.existing_tank_percentage),
            'odo_meter_current_value': self.odo_meter_current_value,
            'driving_type': self.driving_type,
            'location': self.location,
            'fuel_price': float(self.fuel_price),
            'fuel_price_per_liter': self.fuel_price_per_liter,
            'calculated_fuel_added': float(self.calculated_fuel_added),
            'total_cost': float(self.total_cost),
            'km_driven_since_last': self.km_driven_since_last,
            'actual_consumption_l_100km': float(self.actual_consumption_l_100km),
            'fuel_efficiency_rating': self.fuel_efficiency_rating,
            'cost_per_km': self.cost_per_km,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_analysis:
            # Add analysis data like trends, comparisons, etc.
            vehicle_records = FuelRecord.get_vehicle_records(self.vehicle_id, limit=10)
            if len(vehicle_records) > 1:
                recent_avg = sum(r.actual_consumption_l_100km for r in vehicle_records[:5]) / 5
                data['recent_average_consumption'] = float(recent_avg)
                data['consumption_trend'] = 'improving' if self.actual_consumption_l_100km < recent_avg else 'declining'
        
        return data
    
    @classmethod
    def get_vehicle_records(cls, vehicle_id, limit=None, days=None):
        """Get fuel records for a vehicle"""
        query = cls.query.filter_by(vehicle_id=vehicle_id)
        
        if days:
            cutoff_date = date.today() - timedelta(days=days)
            query = query.filter(cls.record_date >= cutoff_date)
        
        query = query.order_by(db.desc(cls.record_date), db.desc(cls.record_time))
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    @classmethod
    def get_latest_odometer(cls, vehicle_id):
        """Get latest odometer reading for a vehicle"""
        latest_record = cls.query.filter_by(vehicle_id=vehicle_id).order_by(
            db.desc(cls.record_date), db.desc(cls.record_time)
        ).first()
        
        return latest_record.odo_meter_current_value if latest_record else None
    
    @classmethod
    def validate_new_odometer(cls, vehicle_id, new_odometer):
        """Validate new odometer reading"""
        latest_odometer = cls.get_latest_odometer(vehicle_id)
        if latest_odometer and new_odometer < latest_odometer:
            return False, f"New odometer reading ({new_odometer}) cannot be less than latest reading ({latest_odometer})"
        return True, None
    
    def __repr__(self):
        return f'<FuelRecord {self.id}: {self.vehicle_id} on {self.record_date}>'