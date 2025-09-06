-- Fix ml_predictions table schema by adding missing columns

USE autoguardian_fuel_system;

-- Add missing columns to ml_predictions table
ALTER TABLE ml_predictions 
ADD COLUMN IF NOT EXISTS model_version VARCHAR(20) DEFAULT '1.0',
ADD COLUMN IF NOT EXISTS confidence_score DECIMAL(3,2) DEFAULT NULL,
ADD COLUMN IF NOT EXISTS prediction_source VARCHAR(50) DEFAULT 'random_forest',
ADD COLUMN IF NOT EXISTS annual_fuel_cost DECIMAL(8,2) DEFAULT NULL,
ADD COLUMN IF NOT EXISTS annual_co2_emissions DECIMAL(10,2) DEFAULT NULL,
ADD COLUMN IF NOT EXISTS mpg_equivalent DECIMAL(5,1) DEFAULT NULL,
ADD COLUMN IF NOT EXISTS prediction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
ADD INDEX IF NOT EXISTS idx_prediction_date (prediction_date);

-- Show the updated table structure
DESCRIBE ml_predictions;