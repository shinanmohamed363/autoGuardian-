#!/usr/bin/env python3
"""
Fix database schema issues
"""

import pymysql
from config import config

def fix_ml_predictions_table():
    """Add missing columns to ml_predictions table"""
    
    # Get database configuration
    db_config = config['development']()
    
    # Parse database URL to get connection parameters  
    db_url = db_config.SQLALCHEMY_DATABASE_URI
    # Format: mysql+pymysql://user:password@host:port/database
    print(f"Database URL: {db_url}")
    
    # Extract connection details
    import re
    match = re.match(r'mysql\+pymysql://([^:]+):([^@]*)@([^:]+):?(\d+)?/(.+)', db_url)
    if not match:
        print("Error: Could not parse database URL")
        return False
        
    user, password, host, port, database = match.groups()
    port = int(port) if port else 3306
    
    try:
        # Connect to database
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            print("Connected to database successfully!")
            
            # Check current table structure
            cursor.execute("DESCRIBE ml_predictions")
            current_columns = [row[0] for row in cursor.fetchall()]
            print(f"Current columns: {current_columns}")
            
            # List of columns that should exist
            required_columns = {
                'model_version': "VARCHAR(20) DEFAULT '1.0'",
                'confidence_score': "DECIMAL(3,2) DEFAULT NULL", 
                'prediction_source': "VARCHAR(50) DEFAULT 'random_forest'",
                'annual_fuel_cost': "DECIMAL(8,2) DEFAULT NULL",
                'annual_co2_emissions': "DECIMAL(10,2) DEFAULT NULL",
                'mpg_equivalent': "DECIMAL(5,1) DEFAULT NULL",
                'prediction_date': "DATETIME DEFAULT CURRENT_TIMESTAMP",
                'created_at': "DATETIME DEFAULT CURRENT_TIMESTAMP"
            }
            
            # Add missing columns
            for column, definition in required_columns.items():
                if column not in current_columns:
                    alter_query = f"ALTER TABLE ml_predictions ADD COLUMN {column} {definition}"
                    print(f"Adding column: {column}")
                    cursor.execute(alter_query)
                else:
                    print(f"Column {column} already exists")
            
            # Add index on prediction_date if it doesn't exist
            try:
                cursor.execute("ALTER TABLE ml_predictions ADD INDEX idx_prediction_date (prediction_date)")
                print("Added index on prediction_date")
            except pymysql.Error as e:
                if "Duplicate key name" in str(e):
                    print("Index on prediction_date already exists")
                else:
                    print(f"Error adding index: {e}")
            
            # Commit changes
            connection.commit()
            print("Schema updates completed successfully!")
            
            # Show updated structure
            cursor.execute("DESCRIBE ml_predictions")
            updated_columns = cursor.fetchall()
            print("\nUpdated table structure:")
            for column in updated_columns:
                print(f"  {column[0]}: {column[1]}")
                
        connection.close()
        return True
        
    except Exception as e:
        print(f"Database error: {e}")
        return False

if __name__ == '__main__':
    success = fix_ml_predictions_table()
    if success:
        print("\nDatabase schema fixed successfully!")
    else:
        print("\nFailed to fix database schema!")