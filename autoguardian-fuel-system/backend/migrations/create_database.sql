-- AutoGuardian Fuel Management System - Database Schema
-- MariaDB/MySQL Database Creation Script

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS autoguardian_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE autoguardian_db;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes for performance
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_active (is_active)
);

-- Enhanced Vehicles Table
CREATE TABLE IF NOT EXISTS vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    vehicle_id VARCHAR(50) UNIQUE NOT NULL,
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
    starting_odometer_value INT NOT NULL DEFAULT 0,
    odo_meter_when_buy_vehicle INT NOT NULL DEFAULT 0,
    full_tank_capacity DECIMAL(5,2) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    -- Indexes for performance
    INDEX idx_vehicle_id (vehicle_id),
    INDEX idx_user_vehicle (user_id, vehicle_id),
    INDEX idx_make_model (make, model),
    INDEX idx_active (is_active)
);

-- Enhanced Fuel Records Table
CREATE TABLE IF NOT EXISTS fuel_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id VARCHAR(50) NOT NULL,
    record_date DATE NOT NULL,
    record_time TIME NOT NULL,
    existing_tank_percentage DECIMAL(5,2) NOT NULL CHECK (existing_tank_percentage >= 0 AND existing_tank_percentage <= 100),
    after_refuel_percentage DECIMAL(5,2) NOT NULL CHECK (after_refuel_percentage >= 0 AND after_refuel_percentage <= 100),
    odo_meter_current_value INT NOT NULL,
    driving_type ENUM('city', 'highway', 'mix') NOT NULL,
    location VARCHAR(100) NOT NULL,
    fuel_price DECIMAL(6,2) NOT NULL,
    calculated_fuel_added DECIMAL(6,2) DEFAULT 0,
    total_cost DECIMAL(8,2) DEFAULT 0,
    km_driven_since_last INT DEFAULT 0,
    actual_consumption_l_100km DECIMAL(6,2) DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id) ON DELETE CASCADE,
    
    -- Indexes for performance
    INDEX idx_vehicle_date (vehicle_id, record_date),
    INDEX idx_driving_type (driving_type),
    INDEX idx_location (location),
    INDEX idx_consumption (actual_consumption_l_100km)
);

-- ML Predictions Table
CREATE TABLE IF NOT EXISTS ml_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id VARCHAR(50) NOT NULL,
    combined_l_100km DECIMAL(6,2),
    highway_l_100km DECIMAL(6,2),
    city_l_100km DECIMAL(6,2),
    emissions_g_km DECIMAL(8,2),
    efficiency_rating VARCHAR(50),
    confidence_score DECIMAL(3,2),
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id) ON DELETE CASCADE,
    
    -- Indexes
    INDEX idx_vehicle_prediction (vehicle_id, prediction_date)
);

-- AI Recommendations Table
CREATE TABLE IF NOT EXISTS ai_recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    vehicle_id VARCHAR(50) NOT NULL,
    recommendation_type ENUM('daily', 'weekly', 'monthly', 'maintenance', 'efficiency') NOT NULL,
    recommendation_title VARCHAR(200) NOT NULL,
    recommendation_text TEXT NOT NULL,
    performance_analysis TEXT,
    priority_level ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    is_read BOOLEAN DEFAULT FALSE,
    is_implemented BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id) ON DELETE CASCADE,
    
    -- Indexes
    INDEX idx_user_recommendations (user_id, created_at),
    INDEX idx_vehicle_recommendations (vehicle_id, recommendation_type),
    INDEX idx_priority (priority_level, is_read)
);

-- Vehicle Statistics Table (for caching performance metrics)
CREATE TABLE IF NOT EXISTS vehicle_statistics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id VARCHAR(50) NOT NULL,
    total_fuel_consumed DECIMAL(10,2) DEFAULT 0,
    total_distance_driven INT DEFAULT 0,
    total_cost DECIMAL(10,2) DEFAULT 0,
    average_consumption DECIMAL(6,2) DEFAULT 0,
    last_fuel_record_date DATE,
    total_refuels INT DEFAULT 0,
    efficiency_trend VARCHAR(20) DEFAULT 'stable',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id) ON DELETE CASCADE,
    
    -- Indexes
    UNIQUE INDEX idx_vehicle_stats (vehicle_id)
);

-- User Preferences Table
CREATE TABLE IF NOT EXISTS user_preferences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    distance_unit ENUM('km', 'miles') DEFAULT 'km',
    volume_unit ENUM('liters', 'gallons') DEFAULT 'liters',
    date_format VARCHAR(20) DEFAULT 'YYYY-MM-DD',
    notification_email BOOLEAN DEFAULT TRUE,
    notification_maintenance BOOLEAN DEFAULT TRUE,
    notification_efficiency BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    -- Indexes
    UNIQUE INDEX idx_user_prefs (user_id)
);

-- Create triggers for automatic calculations in fuel_records
DELIMITER //

CREATE TRIGGER fuel_record_calculations
    BEFORE INSERT ON fuel_records
    FOR EACH ROW
BEGIN
    DECLARE tank_capacity DECIMAL(5,2);
    
    -- Get tank capacity for the vehicle
    SELECT full_tank_capacity INTO tank_capacity 
    FROM vehicles 
    WHERE vehicle_id = NEW.vehicle_id;
    
    -- Calculate fuel added
    SET NEW.calculated_fuel_added = 
        ((NEW.after_refuel_percentage - NEW.existing_tank_percentage) / 100) * tank_capacity;
    
    -- Calculate total cost
    SET NEW.total_cost = NEW.calculated_fuel_added * NEW.fuel_price / 100;
END//

CREATE TRIGGER fuel_record_calculations_update
    BEFORE UPDATE ON fuel_records
    FOR EACH ROW
BEGIN
    DECLARE tank_capacity DECIMAL(5,2);
    
    -- Get tank capacity for the vehicle
    SELECT full_tank_capacity INTO tank_capacity 
    FROM vehicles 
    WHERE vehicle_id = NEW.vehicle_id;
    
    -- Calculate fuel added
    SET NEW.calculated_fuel_added = 
        ((NEW.after_refuel_percentage - NEW.existing_tank_percentage) / 100) * tank_capacity;
    
    -- Calculate total cost
    SET NEW.total_cost = NEW.calculated_fuel_added * NEW.fuel_price / 100;
END//

DELIMITER ;

-- Insert sample data for testing
INSERT INTO users (username, email, password_hash, first_name, last_name) VALUES
('testuser', 'test@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj7.k3K6nDfW', 'Test', 'User'),
('demo', 'demo@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj7.k3K6nDfW', 'Demo', 'User');

-- Sample vehicle data
INSERT INTO vehicles (user_id, vehicle_id, vehicle_name, make, model, year, vehicle_class, 
                     engine_size, cylinders, transmission, fuel_type, tank_capacity, 
                     starting_odometer_value, odo_meter_when_buy_vehicle, full_tank_capacity) VALUES
(1, 'BMW_01', 'My BMW X5', 'BMW', 'X5', 2023, 'SUV: SMALL', 3.0, 6, 'A8', 'Z', 83.0, 10000, 10000, 83.0),
(1, 'TOYOTA_01', 'My Toyota Camry', 'TOYOTA', 'CAMRY', 2022, 'COMPACT', 2.5, 4, 'A6', 'X', 60.0, 5000, 5000, 60.0);

-- Initialize user preferences
INSERT INTO user_preferences (user_id) VALUES (1), (2);

-- Initialize vehicle statistics
INSERT INTO vehicle_statistics (vehicle_id) VALUES ('BMW_01'), ('TOYOTA_01');

COMMIT;