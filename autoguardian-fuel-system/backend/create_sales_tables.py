"""
Create vehicle sales and negotiation tables
"""

from app import create_app
from database import db
from models.vehicle_sale import VehicleSale, Negotiation

def create_tables():
    """Create the vehicle sales and negotiation tables"""
    try:
        app = create_app()
        
        with app.app_context():
            print("Creating vehicle sales tables...")
            
            # Create the tables
            db.create_all()
            
            print("✅ Vehicle sales tables created successfully!")
            print("Tables created:")
            print("- vehicle_sales")
            print("- negotiations")
            
            # Verify tables exist
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'vehicle_sales' in tables:
                print("✅ vehicle_sales table exists")
            else:
                print("❌ vehicle_sales table not found")
            
            if 'negotiations' in tables:
                print("✅ negotiations table exists")
            else:
                print("❌ negotiations table not found")
                
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

if __name__ == '__main__':
    create_tables()