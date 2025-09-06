#!/usr/bin/env python3
"""
Simple script to recreate the database schema with the new vehicle structure
WARNING: This will delete all existing data!
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

def recreate_schema():
    """Recreate the database schema"""
    try:
        # Connect to database
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("Recreating database schema...")
        print("WARNING: This will delete all existing data!")
        
        # Drop all tables in correct order (due to foreign keys)
        print("1. Dropping existing tables...")
        drop_tables = [
            "DROP TABLE IF EXISTS fuel_records",
            "DROP TABLE IF EXISTS ml_predictions", 
            "DROP TABLE IF EXISTS ai_recommendations",
            "DROP TABLE IF EXISTS vehicle_statistics",
            "DROP TABLE IF EXISTS vehicles"
        ]
        
        for drop_sql in drop_tables:
            cursor.execute(drop_sql)
            print(f"  OK {drop_sql}")
        
        print("2. Creating tables with new schema...")
        
        # Create vehicles table (without vehicle_id column)
        vehicles_sql = """
        CREATE TABLE vehicles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            vehicle_name VARCHAR(100) NOT NULL,
            make VARCHAR(50) NOT NULL,
            model VARCHAR(50) NOT NULL,
            year INT NOT NULL,
            vehicle_class VARCHAR(50) NOT NULL,
            engine_size DECIMAL(3,1) NOT NULL,
            cylinders INT NOT NULL,
            transmission VARCHAR(20) NOT NULL,
            fuel_type VARCHAR(20) NOT NULL,
            tank_capacity DECIMAL(5,2) NOT NULL,
            starting_odometer_value INT DEFAULT 0,
            odo_meter_when_buy_vehicle INT DEFAULT 0,
            full_tank_capacity DECIMAL(5,2) NOT NULL,
            initial_tank_percentage DECIMAL(5,2) DEFAULT 100.0,
            is_active BOOLEAN DEFAULT TRUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_user_id (user_id),
            INDEX idx_make (make),
            INDEX idx_model (model),
            INDEX idx_active (is_active),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
        cursor.execute(vehicles_sql)
        print("  OK Created vehicles table")
        
        # Create vehicle_statistics table
        stats_sql = """
        CREATE TABLE vehicle_statistics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            vehicle_id INT NOT NULL UNIQUE,
            total_fuel_consumed DECIMAL(10,2) DEFAULT 0,
            total_distance_driven INT DEFAULT 0,
            total_cost DECIMAL(10,2) DEFAULT 0,
            average_consumption DECIMAL(6,2) DEFAULT 0,
            last_fuel_record_date DATE,
            total_refuels INT DEFAULT 0,
            efficiency_trend VARCHAR(20) DEFAULT 'stable',
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
        )
        """
        cursor.execute(stats_sql)
        print("  OK Created vehicle_statistics table")
        
        # Create fuel_records table
        fuel_sql = """
        CREATE TABLE fuel_records (
            id INT AUTO_INCREMENT PRIMARY KEY,
            vehicle_id INT NOT NULL,
            record_date DATE NOT NULL,
            record_time TIME NOT NULL,
            existing_tank_percentage DECIMAL(5,2) NOT NULL,
            after_refuel_percentage DECIMAL(5,2) NOT NULL,
            odo_meter_current_value INT NOT NULL,
            driving_type ENUM('city', 'highway', 'mix') NOT NULL,
            location VARCHAR(100) NOT NULL,
            fuel_price DECIMAL(6,2) NOT NULL,
            calculated_fuel_added DECIMAL(6,2) DEFAULT 0,
            total_cost DECIMAL(8,2) DEFAULT 0,
            km_driven_since_last INT DEFAULT 0,
            actual_consumption_l_100km DECIMAL(6,2) DEFAULT 0,
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_vehicle_id (vehicle_id),
            INDEX idx_record_date (record_date),
            INDEX idx_driving_type (driving_type),
            INDEX idx_location (location),
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
        )
        """
        cursor.execute(fuel_sql)
        print("  OK Created fuel_records table")
        
        # Create ml_predictions table
        ml_sql = """
        CREATE TABLE ml_predictions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            vehicle_id INT NOT NULL,
            combined_l_100km DECIMAL(6,2),
            highway_l_100km DECIMAL(6,2),
            city_l_100km DECIMAL(6,2),
            emissions_g_km DECIMAL(8,2),
            efficiency_rating VARCHAR(50),
            model_version VARCHAR(20) DEFAULT '1.0',
            confidence_score DECIMAL(3,2),
            prediction_source VARCHAR(50) DEFAULT 'random_forest',
            annual_fuel_cost DECIMAL(8,2),
            annual_co2_emissions DECIMAL(10,2),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_vehicle_id (vehicle_id),
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
        )
        """
        cursor.execute(ml_sql)
        print("  OK Created ml_predictions table")
        
        # Create ai_recommendations table
        ai_sql = """
        CREATE TABLE ai_recommendations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            vehicle_id INT NOT NULL,
            recommendation_type VARCHAR(20) NOT NULL,
            recommendation_title VARCHAR(200) NOT NULL,
            recommendation_text TEXT NOT NULL,
            performance_analysis TEXT,
            priority_level VARCHAR(20) DEFAULT 'medium',
            category VARCHAR(50),
            impact_score DECIMAL(3,2),
            is_read BOOLEAN DEFAULT FALSE,
            is_implemented BOOLEAN DEFAULT FALSE,
            implementation_notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_user_id (user_id),
            INDEX idx_vehicle_id (vehicle_id),
            INDEX idx_type (recommendation_type),
            INDEX idx_priority (priority_level),
            INDEX idx_read (is_read),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
        )
        """
        cursor.execute(ai_sql)
        print("  OK Created ai_recommendations table")
        
        # Commit all changes
        conn.commit()
        print("\nSUCCESS Schema recreated successfully!")
        print("Note: All previous vehicle data has been deleted.")
        
    except pymysql.Error as e:
        print(f"\nFAILED Schema recreation failed: {e}")
        if conn:
            conn.rollback()
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    print("Database Schema Recreation")
    print("=" * 40)
    print("WARNING: This will delete ALL existing vehicle, fuel record,")
    print("prediction, and recommendation data!")
    print()
    
    response = input("Are you sure you want to continue? (y/N): ")
    if response.lower() != 'y':
        print("Operation cancelled.")
        exit(0)
    
    recreate_schema()