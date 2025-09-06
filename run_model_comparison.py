#!/usr/bin/env python3
"""
Script to run the fuel consumption model comparison and generate the best performing PKL model.
This script executes the same code as in the Jupyter notebook but in a Python script format.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.multioutput import MultiOutputRegressor
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)

def load_data(filepath):
    """Load data from CSV file."""
    print(f"Loading data from {filepath}...")
    try:
        # Read data
        df = pd.read_csv(filepath)
        print(f"Data loaded successfully. Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def explore_data(df):
    """Explore and visualize the dataset."""
    print("\n" + "="*50)
    print("DATA EXPLORATION")
    print("="*50)
    
    print(f"\nDataset Shape: {df.shape}")
    print(f"\nColumn Names: {list(df.columns)}")
    
    # Display basic statistics
    print("\nBasic Statistics:")
    print(df.describe())
    
    # Check data types
    print("\nData Types:")
    print(df.dtypes)
    
    # Check for missing values
    missing = df.isnull().sum()
    print(f"\nMissing Values:\n{missing[missing > 0]}")
    
    return df

def preprocess_data(df, input_features, output_features):
    """
    Preprocess the data for modeling.
    
    Args:
        df: DataFrame containing the vehicle data
        input_features: List of feature columns to use for prediction
        output_features: List of target columns to predict
    
    Returns:
        X_train, X_test, y_train, y_test, preprocessor
    """
    print("\n" + "="*50)
    print("DATA PREPROCESSING")
    print("="*50)
    
    # Select relevant columns
    data = df[input_features + output_features].copy()
    
    # Check for missing values
    missing = data.isnull().sum()
    print(f"\nMissing values per column:\n{missing[missing > 0]}")
    
    # Drop rows with missing values
    data_clean = data.dropna()
    print(f"Shape after dropping missing values: {data_clean.shape}")
    
    # Separate features and targets
    X = data_clean[input_features]
    y = data_clean[output_features]
    
    # Identify categorical and numerical features
    categorical_features = X.select_dtypes(include=['object']).columns.tolist()
    numerical_features = X.select_dtypes(include=['number']).columns.tolist()
    
    print(f"\nCategorical features: {categorical_features}")
    print(f"Numerical features: {numerical_features}")
    
    # Create preprocessor for feature transformation
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
        ],
        remainder='passthrough'
    )
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"\nTraining set size: {X_train.shape[0]}")
    print(f"Testing set size: {X_test.shape[0]}")
    
    return X_train, X_test, y_train, y_test, preprocessor, categorical_features, numerical_features

def compare_models(X_train, X_test, y_train, y_test, preprocessor, output_features):
    """
    Compare multiple machine learning models and return the best performing one.
    
    Args:
        X_train: Training features
        X_test: Test features
        y_train: Training targets
        y_test: Test targets
        preprocessor: Column transformer for preprocessing
        output_features: Names of target features
    
    Returns:
        Dictionary containing trained models, metrics, and best model
    """
    print("\n" + "="*50)
    print("MODEL COMPARISON")
    print("="*50)
    
    # Define models with appropriate parameters
    models = {
        'Random Forest': MultiOutputRegressor(RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )),
        'Decision Tree': MultiOutputRegressor(DecisionTreeRegressor(
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )),
        'Neural Network': MultiOutputRegressor(MLPRegressor(
            hidden_layer_sizes=(100, 50),
            max_iter=500,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1
        )),
        'Logistic Regression': MultiOutputRegressor(LogisticRegression(
            max_iter=1000,
            random_state=42
        ))
    }
    
    # Create pipelines and train models
    trained_models = {}
    all_metrics = {}
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        
        # Create pipeline
        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('scaler', StandardScaler()),
            ('model', model)
        ])
        
        try:
            # Train the model
            pipeline.fit(X_train, y_train)
            
            # Make predictions
            y_pred = pipeline.predict(X_test)
            
            # Convert to DataFrame if needed
            if isinstance(y_pred, np.ndarray):
                y_pred = pd.DataFrame(y_pred, columns=output_features)
            
            # Calculate metrics
            model_metrics = {}
            total_r2 = 0
            total_rmse = 0
            
            for i, col in enumerate(output_features):
                rmse = np.sqrt(mean_squared_error(y_test[col], y_pred[col]))
                mae = mean_absolute_error(y_test[col], y_pred[col])
                r2 = r2_score(y_test[col], y_pred[col])
                
                model_metrics[col] = {
                    'rmse': rmse,
                    'mae': mae,
                    'r2': r2
                }
                
                total_r2 += r2
                total_rmse += rmse
            
            # Calculate average metrics
            avg_r2 = total_r2 / len(output_features)
            avg_rmse = total_rmse / len(output_features)
            
            model_metrics['average'] = {
                'r2': avg_r2,
                'rmse': avg_rmse
            }
            
            trained_models[name] = pipeline
            all_metrics[name] = model_metrics
            
            print(f"{name} - Average R²: {avg_r2:.4f}, Average RMSE: {avg_rmse:.4f}")
            
        except Exception as e:
            print(f"Error training {name}: {str(e)}")
            continue
    
    # Find best model based on average R² score
    best_model_name = max(all_metrics.keys(), key=lambda x: all_metrics[x]['average']['r2'])
    best_model = trained_models[best_model_name]
    
    print(f"\nBest performing model: {best_model_name}")
    print(f"Best model Average R²: {all_metrics[best_model_name]['average']['r2']:.4f}")
    print(f"Best model Average RMSE: {all_metrics[best_model_name]['average']['rmse']:.4f}")
    
    return {
        'trained_models': trained_models,
        'metrics': all_metrics,
        'best_model': best_model,
        'best_model_name': best_model_name
    }

def save_best_model(best_model, best_model_name, output_dir='model'):
    """
    Save the best performing model as a PKL file.
    
    Args:
        best_model: Best performing trained model
        best_model_name: Name of the best model
        output_dir: Directory to save the model
    
    Returns:
        Path to saved model file
    """
    print(f"\nSaving best model ({best_model_name}) to PKL file...")
    
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create filename
    model_filename = f'best_fuel_model_{best_model_name.lower().replace(" ", "_")}.pkl'
    model_path = os.path.join(output_dir, model_filename)
    
    # Save the model
    joblib.dump(best_model, model_path)
    print(f"Best model saved successfully to: {model_path}")
    
    return model_path

def main():
    """Main function to execute the enhanced workflow with model comparison."""
    print("="*60)
    print("ENHANCED FUEL CONSUMPTION PREDICTION WITH MODEL COMPARISON")
    print("="*60)
    
    # Define file path
    file_path = 'dataset/Fuel_Consumption_2000-2022.csv'
    
    # Define input and output features based on actual CSV column names
    input_features = [
        'MAKE', 'MODEL', 'VEHICLE CLASS', 
        'ENGINE SIZE', 'CYLINDERS', 'TRANSMISSION', 'FUEL'
    ]
    
    # Check if CSV file exists and read columns
    if os.path.exists(file_path):
        df_temp = pd.read_csv(file_path)
        # Updated to include highway consumption if available
        if 'HWY (L/100 km)' in df_temp.columns:
            output_features = ['COMB (L/100 km)', 'HWY (L/100 km)', 'EMISSIONS']
        else:
            output_features = ['COMB (L/100 km)', 'EMISSIONS']
    else:
        output_features = ['COMB (L/100 km)', 'EMISSIONS']
    
    # Load data
    df = load_data(file_path)
    
    if df is not None:
        # Explore data
        df = explore_data(df)
        
        # Preprocess data
        X_train, X_test, y_train, y_test, preprocessor, categorical_features, numerical_features = preprocess_data(
            df, input_features, output_features)
        
        # Compare multiple models
        model_comparison = compare_models(X_train, X_test, y_train, y_test, preprocessor, output_features)
        
        # Get the best model
        best_model = model_comparison['best_model']
        best_model_name = model_comparison['best_model_name']
        all_metrics = model_comparison['metrics']
        
        # Save the best model as PKL file
        model_path = save_best_model(best_model, best_model_name)
        
        # Display final results
        print(f"\n" + "="*50)
        print("FINAL RESULTS")
        print("="*50)
        print(f"Best performing model: {best_model_name}")
        print(f"Model saved to: {model_path}")
        
        # Print detailed metrics for all models
        print(f"\nDETAILED METRICS FOR ALL MODELS:")
        print("-" * 50)
        for model_name, metrics in all_metrics.items():
            print(f"\n{model_name}:")
            print(f"  Average R²: {metrics['average']['r2']:.4f}")
            print(f"  Average RMSE: {metrics['average']['rmse']:.4f}")
            for feature in output_features:
                if feature in metrics:
                    print(f"  {feature} - R²: {metrics[feature]['r2']:.4f}, RMSE: {metrics[feature]['rmse']:.4f}")
        
        print(f"\nModel training and evaluation completed successfully!")
        return best_model, all_metrics, model_path
    
    else:
        print("Failed to load data. Please check the file path.")
        return None, None, None

if __name__ == "__main__":
    model, metrics, model_path = main()