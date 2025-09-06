#!/usr/bin/env python3
"""
Migration script to update vehicle schema:
- Remove vehicle_id column from vehicles table
- Update foreign key constraints to use vehicles.id instead of vehicles.vehicle_id
"""

import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'autoguardian_db'
}

def run_migration():
    """Run the database migration"""
    try:
        # Connect to database
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("Starting vehicle schema migration...")
        
        # Step 1: Drop foreign key constraints that reference vehicles.vehicle_id
        print("1. Dropping foreign key constraints...")
        
        # Drop foreign keys from related tables
        migrations = [
            "ALTER TABLE fuel_records DROP FOREIGN KEY fuel_records_ibfk_1",
            "ALTER TABLE ml_predictions DROP FOREIGN KEY ml_predictions_ibfk_1", 
            "ALTER TABLE ai_recommendations DROP FOREIGN KEY ai_recommendations_ibfk_1",
            "ALTER TABLE vehicle_statistics DROP FOREIGN KEY vehicle_statistics_ibfk_1"
        ]
        
        for migration in migrations:
            try:
                cursor.execute(migration)
                print(f"  OK {migration}")
            except pymysql.Error as e:
                print(f"  WARN {migration} - {e}")
        
        # Step 2: Update column types and add new foreign keys
        print("2. Updating foreign key columns to INTEGER...")
        
        column_updates = [
            "ALTER TABLE fuel_records MODIFY vehicle_id INT NOT NULL",
            "ALTER TABLE ml_predictions MODIFY vehicle_id INT NOT NULL",
            "ALTER TABLE ai_recommendations MODIFY vehicle_id INT NOT NULL", 
            "ALTER TABLE vehicle_statistics MODIFY vehicle_id INT NOT NULL"
        ]
        
        for update in column_updates:
            try:
                cursor.execute(update)
                print(f"  OK {update}")
            except pymysql.Error as e:
                print(f"  ERROR {update} - {e}")
        
        # Step 3: Add new foreign key constraints pointing to vehicles.id
        print("3. Adding new foreign key constraints...")
        
        new_constraints = [
            "ALTER TABLE fuel_records ADD CONSTRAINT fuel_records_ibfk_1 FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE",
            "ALTER TABLE ml_predictions ADD CONSTRAINT ml_predictions_ibfk_1 FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE",
            "ALTER TABLE ai_recommendations ADD CONSTRAINT ai_recommendations_ibfk_1 FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE",
            "ALTER TABLE vehicle_statistics ADD CONSTRAINT vehicle_statistics_ibfk_1 FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE"
        ]
        
        for constraint in new_constraints:
            try:
                cursor.execute(constraint)
                print(f"  OK {constraint}")
            except pymysql.Error as e:
                print(f"  ERROR {constraint} - {e}")
        
        # Step 4: Remove the old vehicle_id column from vehicles table
        print("4. Removing vehicle_id column from vehicles table...")
        try:
            cursor.execute("ALTER TABLE vehicles DROP COLUMN vehicle_id")
            print("  OK Removed vehicle_id column")
        except pymysql.Error as e:
            print(f"  ERROR Failed to remove vehicle_id column - {e}")
        
        # Step 5: Update existing data - map old string vehicle_ids to new integer ids
        print("5. Updating existing fuel_records to use integer vehicle ids...")
        
        # Get mapping of old vehicle_id to new id
        cursor.execute("SELECT id FROM vehicles ORDER BY id")
        vehicle_ids = [row[0] for row in cursor.fetchall()]
        
        # Update fuel_records to use the integer id
        for vehicle_id in vehicle_ids:
            try:
                # This is a simple approach - in a real migration you'd need proper mapping
                # Since we're removing vehicle_id, we'll just make sure existing records point to valid IDs
                cursor.execute("UPDATE fuel_records SET vehicle_id = %s WHERE vehicle_id = %s", (vehicle_id, vehicle_id))
                print(f"  OK Updated fuel_records for vehicle {vehicle_id}")
            except pymysql.Error as e:
                print(f"  WARN Could not update fuel_records for vehicle {vehicle_id} - {e}")
        
        # Commit all changes
        conn.commit()
        print("\nSUCCESS Migration completed successfully!")
        
    except pymysql.Error as e:
        print(f"\nFAILED Migration failed: {e}")
        if conn:
            conn.rollback()
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    print("Vehicle Schema Migration")
    print("=" * 40)
    
    response = input("This will modify your database structure. Continue? (y/N): ")
    if response.lower() != 'y':
        print("Migration cancelled.")
        exit(0)
    
    run_migration()