import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import joblib
import warnings
import google.generativeai as genai
from collections import defaultdict
warnings.filterwarnings('ignore')

# Configure Google Generative AI
genai.configure(api_key="AIzaSyCTSwSJgM3xfBNz2xcLHBhAb2Fn1YTl0So")

class VehicleFuelTracker:
    def __init__(self, model_path='model/enhanced_fuel_model.joblib'):
        """Initialize the fuel tracking system."""
        self.model = None
        self.load_model(model_path)
        self.vehicle_data = {}
        self.fuel_records = []
        
    def load_model(self, model_path):
        """Load the trained fuel consumption model."""
        try:
            self.model = joblib.load(model_path)
            print("Model loaded successfully!")
        except FileNotFoundError:
            print(f"Model not found at {model_path}. Please train the model first.")
            
    def add_vehicle(self, vehicle_data):
        """Add a vehicle to the tracking system."""
        vehicle_id = vehicle_data['vehicle_id']
        self.vehicle_data[vehicle_id] = vehicle_data
        print(f"Vehicle {vehicle_id} added successfully!")
        
    def add_fuel_record(self, fuel_record):
        """Add a fuel record to the system with ODO meter validation."""
        # Validate ODO meter reading
        vehicle_id = fuel_record['vehicle_id']
        current_odo = fuel_record['ODO_meter_current_value']
        
        # Check if this is the first record or ODO is increasing
        vehicle_records = [r for r in self.fuel_records if r['vehicle_id'] == vehicle_id]
        if vehicle_records:
            last_odo = max([r['ODO_meter_current_value'] for r in vehicle_records])
            if current_odo < last_odo:
                print(f"Warning: ODO meter reading ({current_odo}) is less than previous reading ({last_odo})")
                return False
        
        # Calculate fuel added based on tank percentages
        vehicle = self.vehicle_data.get(vehicle_id)
        if vehicle:
            tank_capacity = vehicle['full_tank_capacity']
            fuel_percentage_added = fuel_record['after_refuel_percentage'] - fuel_record['existing_tank_percentage']
            calculated_fuel_added = (fuel_percentage_added / 100) * tank_capacity
            fuel_record['calculated_fuel_added'] = round(calculated_fuel_added, 2)
            
            # Calculate kilometers driven since last refuel
            if vehicle_records:
                # Find the most recent previous record
                previous_record = max(vehicle_records, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
                km_driven = current_odo - previous_record['ODO_meter_current_value']
                fuel_record['km_driven_since_last'] = km_driven
                
                # Calculate actual fuel consumption rate (L/100km)
                if km_driven > 0:
                    consumption_rate = (calculated_fuel_added / km_driven) * 100
                    fuel_record['actual_consumption_l_100km'] = round(consumption_rate, 2)
                else:
                    fuel_record['actual_consumption_l_100km'] = 0
            else:
                # First record - calculate from initial ODO when vehicle was purchased
                initial_odo = vehicle.get('ODO_meter_when_buy_vehicle', 0)
                km_driven = current_odo - initial_odo
                fuel_record['km_driven_since_last'] = km_driven
                
                if km_driven > 0:
                    consumption_rate = (calculated_fuel_added / km_driven) * 100
                    fuel_record['actual_consumption_l_100km'] = round(consumption_rate, 2)
                else:
                    fuel_record['actual_consumption_l_100km'] = 0
        
        self.fuel_records.append(fuel_record)
        print(f"Fuel record added: {fuel_record.get('calculated_fuel_added', 0)}L, {fuel_record.get('km_driven_since_last', 0)}km driven")
        return True
        
    def predict_vehicle_consumption(self, vehicle_id):
        """Predict fuel consumption for a specific vehicle using the ML model."""
        if self.model is None:
            return None
            
        vehicle = self.vehicle_data.get(vehicle_id)
        if not vehicle:
            return None
            
        # Map vehicle data to model input format
        model_input = {
            'MAKE': vehicle['Make'],
            'MODEL': vehicle['Model'],
            'VEHICLE CLASS': vehicle['Vehicle Class'],
            'ENGINE SIZE': float(vehicle['Engine Size'].replace(' L', '')),
            'CYLINDERS': vehicle['Cylinders'],
            'TRANSMISSION': self._map_transmission(vehicle['Transmission']),
            'FUEL': self._map_fuel_type(vehicle['Fuel Type'])
        }
        
        try:
            input_df = pd.DataFrame([model_input])
            predictions = self.model.predict(input_df)
            
            combined_consumption = predictions[0][0]
            emissions = predictions[0][1]
            
            # Estimate different driving conditions
            highway_consumption = combined_consumption * 0.85
            city_consumption = combined_consumption * 1.20
            
            return {
                'combined': round(combined_consumption, 2),
                'highway': round(highway_consumption, 2),
                'city': round(city_consumption, 2),
                'emissions': round(emissions, 2)
            }
        except Exception as e:
            print(f"Error predicting consumption: {e}")
            return None
    
    def _map_transmission(self, transmission):
        """Map transmission type to model format."""
        if 'Automatic' in transmission:
            return 'A4'
        elif 'Manual' in transmission:
            return 'M6'
        else:
            return 'AS'
    
    def _map_fuel_type(self, fuel_type):
        """Map fuel type to model format."""
        if 'Regular' in fuel_type:
            return 'X'
        elif 'Premium' in fuel_type:
            return 'Z'
        elif 'Diesel' in fuel_type:
            return 'D'
        else:
            return 'X'
    
    def calculate_actual_consumption(self, vehicle_id, start_date=None, end_date=None):
        """Calculate actual fuel consumption from records using ODO meter data."""
        vehicle_records = [r for r in self.fuel_records if r['vehicle_id'] == vehicle_id]
        
        if start_date:
            vehicle_records = [r for r in vehicle_records if pd.to_datetime(r['date']) >= pd.to_datetime(start_date)]
        if end_date:
            vehicle_records = [r for r in vehicle_records if pd.to_datetime(r['date']) <= pd.to_datetime(end_date)]
        
        if not vehicle_records:
            return None
        
        # Sort records by date
        vehicle_records.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
        
        # Calculate total kilometers and fuel consumption
        total_km = 0
        total_fuel = 0
        total_cost = 0
        driving_stats = defaultdict(lambda: {'fuel': 0, 'cost': 0, 'km': 0, 'records': 0})
        
        for record in vehicle_records:
            fuel_added = record.get('calculated_fuel_added', 0)
            km_driven = record.get('km_driven_since_last', 0)
            cost = fuel_added * record['fuel_price'] / 100  # Convert price from cents
            driving_type = record['driving_type']
            
            driving_stats[driving_type]['fuel'] += fuel_added
            driving_stats[driving_type]['cost'] += cost
            driving_stats[driving_type]['km'] += km_driven
            driving_stats[driving_type]['records'] += 1
            
            total_fuel += fuel_added
            total_cost += cost
            total_km += km_driven
        
        # Calculate overall consumption rate
        overall_consumption = (total_fuel / total_km * 100) if total_km > 0 else 0
        
        return {
            'total_fuel': round(total_fuel, 2),
            'total_cost': round(total_cost, 2),
            'total_km': total_km,
            'overall_consumption_l_100km': round(overall_consumption, 2),
            'driving_stats': dict(driving_stats),
            'period_days': len(set([r['date'] for r in vehicle_records]))
        }
    
    def generate_daily_report(self, vehicle_id, date):
        """Generate daily fuel consumption report with accurate km calculations."""
        daily_records = [r for r in self.fuel_records 
                        if r['vehicle_id'] == vehicle_id and r['date'] == date]
        
        if not daily_records:
            return {"message": "No records found for this date"}
        
        total_fuel = sum([r.get('calculated_fuel_added', 0) for r in daily_records])
        total_cost = sum([r.get('calculated_fuel_added', 0) * r['fuel_price'] / 100 for r in daily_records])
        total_km = sum([r.get('km_driven_since_last', 0) for r in daily_records])
        
        # Calculate actual consumption for the day
        daily_consumption = (total_fuel / total_km * 100) if total_km > 0 else 0
        
        # Get model predictions
        model_predictions = self.predict_vehicle_consumption(vehicle_id)
        
        report = {
            'date': date,
            'vehicle_id': vehicle_id,
            'actual_fuel_consumed': round(total_fuel, 2),
            'actual_cost': round(total_cost, 2),
            'kilometers_driven': total_km,
            'actual_consumption_l_100km': round(daily_consumption, 2),
            'number_of_refuels': len(daily_records),
            'model_predictions': model_predictions,
            'efficiency_status': self._assess_efficiency_with_km(daily_consumption, model_predictions),
            'records': daily_records
        }
        
        return report
    
    def generate_monthly_report(self, vehicle_id, year, month):
        """Generate comprehensive monthly report with accurate km tracking."""
        start_date = f"{year}-{month:02d}-01"
        end_date = f"{year}-{month:02d}-28"  # Simplified
        
        actual_data = self.calculate_actual_consumption(vehicle_id, start_date, end_date)
        model_predictions = self.predict_vehicle_consumption(vehicle_id)
        
        if not actual_data:
            return {"message": "No data found for this month"}
        
        report = {
            'period': f"{year}-{month:02d}",
            'vehicle_id': vehicle_id,
            'total_fuel_consumed': actual_data['total_fuel'],
            'total_cost': actual_data['total_cost'],
            'total_km_driven': actual_data['total_km'],
            'actual_consumption_l_100km': actual_data['overall_consumption_l_100km'],
            'driving_breakdown': actual_data['driving_stats'],
            'model_vs_actual': self._compare_model_actual_with_km(actual_data, model_predictions),
            'efficiency_assessment': self._assess_monthly_efficiency_with_km(actual_data, model_predictions),
            'recommendations': self._get_ai_recommendations(actual_data, model_predictions, 'monthly')
        }
        
        return report
    
    def generate_yearly_forecast(self, vehicle_id, year):
        """Generate yearly forecast and analysis with accurate km data."""
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        
        actual_data = self.calculate_actual_consumption(vehicle_id, start_date, end_date)
        model_predictions = self.predict_vehicle_consumption(vehicle_id)
        
        if not actual_data:
            return {"message": "No data found for this year"}
        
        # Project yearly totals based on actual data
        days_of_data = actual_data['period_days']
        yearly_projection = self._project_yearly_consumption_with_km(actual_data, days_of_data)
        
        report = {
            'year': year,
            'vehicle_id': vehicle_id,
            'actual_data_days': days_of_data,
            'total_km_driven': actual_data['total_km'],
            'actual_consumption_l_100km': actual_data['overall_consumption_l_100km'],
            'projected_yearly_fuel': yearly_projection['fuel'],
            'projected_yearly_cost': yearly_projection['cost'],
            'projected_yearly_km': yearly_projection['km'],
            'projected_yearly_emissions': yearly_projection['emissions'],
            'driving_pattern_analysis': self._analyze_driving_patterns_with_km(actual_data),
            'cost_optimization_tips': self._get_ai_recommendations(actual_data, model_predictions, 'yearly'),
            'maintenance_recommendations': self._get_maintenance_recommendations(actual_data, model_predictions)
        }
        
        return report
    
    def _assess_efficiency_with_km(self, actual_consumption, model_predictions):
        """Assess vehicle efficiency using actual km-based consumption."""
        if not model_predictions or actual_consumption == 0:
            return "Unknown"
        
        expected_consumption = model_predictions['combined']
        difference_pct = ((actual_consumption - expected_consumption) / expected_consumption) * 100
        
        if difference_pct <= -10:
            return "Excellent - Much better than expected"
        elif difference_pct <= 0:
            return "Good - Better than expected"
        elif difference_pct <= 10:
            return "Average - Close to expected"
        else:
            return "Poor - Worse than expected, consider maintenance"
    
    def _compare_model_actual_with_km(self, actual_data, model_predictions):
        """Compare model predictions with actual consumption using km data."""
        if not model_predictions:
            return {"message": "Model predictions not available"}
        
        expected_consumption = model_predictions['combined']
        actual_consumption = actual_data['overall_consumption_l_100km']
        
        difference = actual_consumption - expected_consumption
        percentage_diff = (difference / expected_consumption) * 100
        
        return {
            'expected_consumption_l_100km': expected_consumption,
            'actual_consumption_l_100km': actual_consumption,
            'difference_l_100km': round(difference, 2),
            'percentage_difference': round(percentage_diff, 2),
            'status': 'Better than expected' if difference < 0 else 'Worse than expected',
            'total_km_driven': actual_data['total_km']
        }
    
    def _assess_monthly_efficiency_with_km(self, actual_data, model_predictions):
        """Assess monthly efficiency using accurate km data."""
        comparison = self._compare_model_actual_with_km(actual_data, model_predictions)
        
        if comparison['percentage_difference'] < -10:
            return "Excellent - Vehicle performing much better than expected"
        elif comparison['percentage_difference'] < 0:
            return "Good - Vehicle performing better than expected"
        elif comparison['percentage_difference'] < 10:
            return "Average - Performance close to expectations"
        else:
            return "Poor - Performance worse than expected, maintenance recommended"
    
    def _project_yearly_consumption_with_km(self, actual_data, days_of_data):
        """Project yearly consumption based on actual km and fuel data."""
        daily_avg_fuel = actual_data['total_fuel'] / days_of_data
        daily_avg_cost = actual_data['total_cost'] / days_of_data
        daily_avg_km = actual_data['total_km'] / days_of_data
        
        yearly_fuel = daily_avg_fuel * 365
        yearly_cost = daily_avg_cost * 365
        yearly_km = daily_avg_km * 365
        yearly_emissions = yearly_fuel * 2.3  # Rough CO2 emission factor
        
        return {
            'fuel': round(yearly_fuel, 2),
            'cost': round(yearly_cost, 2),
            'km': round(yearly_km, 2),
            'emissions': round(yearly_emissions, 2)
        }
    
    def _analyze_driving_patterns_with_km(self, actual_data):
        """Analyze driving patterns with accurate km data."""
        driving_stats = actual_data['driving_stats']
        total_fuel = actual_data['total_fuel']
        total_km = actual_data['total_km']
        
        pattern_analysis = {}
        for driving_type, stats in driving_stats.items():
            fuel_percentage = (stats['fuel'] / total_fuel) * 100
            km_percentage = (stats['km'] / total_km) * 100 if total_km > 0 else 0
            consumption_rate = (stats['fuel'] / stats['km'] * 100) if stats['km'] > 0 else 0
            
            pattern_analysis[driving_type] = {
                'fuel_percentage': round(fuel_percentage, 2),
                'km_percentage': round(km_percentage, 2),
                'total_fuel': stats['fuel'],
                'total_km': stats['km'],
                'consumption_l_100km': round(consumption_rate, 2),
                'total_cost': round(stats['cost'], 2),
                'refuel_frequency': stats['records']
            }
        
        return pattern_analysis
    
    def _get_ai_recommendations(self, actual_data, model_predictions, period_type):
        """Get AI-powered recommendations using Google Generative AI."""
        try:
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            prompt = f"""
            As a vehicle efficiency expert, analyze this {period_type} fuel consumption data and provide recommendations:
            
            Actual Fuel Consumption: {actual_data['total_fuel']} liters
            Total Kilometers Driven: {actual_data['total_km']} km
            Actual Consumption Rate: {actual_data['overall_consumption_l_100km']} L/100km
            Total Cost: ${actual_data['total_cost']}
            Driving Patterns: {actual_data['driving_stats']}
            Model Predictions: {model_predictions}
            
            Please provide:
            1. Top 3 cost reduction tips
            2. Efficiency improvement suggestions based on actual vs predicted consumption
            3. Driving behavior recommendations for different driving types
            4. Maintenance suggestions (if applicable)
            
            Keep recommendations practical and specific.
            """
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"AI recommendations unavailable: {str(e)}"
    
    def _get_maintenance_recommendations(self, actual_data, model_predictions):
        """Get maintenance recommendations using AI with km data."""
        try:
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            comparison = self._compare_model_actual_with_km(actual_data, model_predictions)
            
            prompt = f"""
            As an automotive maintenance expert, analyze this vehicle performance data:
            
            Fuel Efficiency Variance: {comparison['percentage_difference']}%
            Actual vs Expected: {comparison['actual_consumption_l_100km']} L/100km vs {comparison['expected_consumption_l_100km']} L/100km
            Total Kilometers Driven: {comparison['total_km_driven']} km
            
            Based on this performance deviation and mileage, recommend:
            1. Specific maintenance tasks needed
            2. Priority level (High/Medium/Low)
            3. Estimated maintenance costs
            4. Expected improvement after maintenance
            5. Mileage-based maintenance schedule
            
            Focus on maintenance items that directly impact fuel efficiency.
            """
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Maintenance recommendations unavailable: {str(e)}"
    
    def visualize_fuel_trends(self, vehicle_id, days=30):
        """Create visualizations for fuel consumption trends with km data."""
        vehicle_records = [r for r in self.fuel_records if r['vehicle_id'] == vehicle_id]
        
        if not vehicle_records:
            print("No records found for visualization")
            return
        
        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame(vehicle_records)
        df['date'] = pd.to_datetime(df['date'])
        df['cost'] = df.get('calculated_fuel_added', 0) * df['fuel_price'] / 100
        
        # Filter recent records
        recent_date = df['date'].max() - timedelta(days=days)
        df_recent = df[df['date'] >= recent_date]
        
        # Create visualizations
        fig, axes = plt.subplots(2, 3, figsize=(20, 12))
        
        # Daily fuel consumption
        daily_fuel = df_recent.groupby('date')['calculated_fuel_added'].sum()
        axes[0, 0].plot(daily_fuel.index, daily_fuel.values, marker='o')
        axes[0, 0].set_title('Daily Fuel Consumption')
        axes[0, 0].set_xlabel('Date')
        axes[0, 0].set_ylabel('Liters')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Daily kilometers driven
        daily_km = df_recent.groupby('date')['km_driven_since_last'].sum()
        axes[0, 1].plot(daily_km.index, daily_km.values, marker='s', color='green')
        axes[0, 1].set_title('Daily Kilometers Driven')
        axes[0, 1].set_xlabel('Date')
        axes[0, 1].set_ylabel('Kilometers')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Daily consumption rate
        daily_consumption = (daily_fuel / daily_km * 100).dropna()
        axes[0, 2].plot(daily_consumption.index, daily_consumption.values, marker='^', color='orange')
        axes[0, 2].set_title('Daily Consumption Rate (L/100km)')
        axes[0, 2].set_xlabel('Date')
        axes[0, 2].set_ylabel('L/100km')
        axes[0, 2].tick_params(axis='x', rotation=45)
        
        # Daily costs
        daily_cost = df_recent.groupby('date')['cost'].sum()
        axes[1, 0].plot(daily_cost.index, daily_cost.values, marker='o', color='red')
        axes[1, 0].set_title('Daily Fuel Costs')
        axes[1, 0].set_xlabel('Date')
        axes[1, 0].set_ylabel('Cost ($)')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Driving type distribution
        driving_dist = df_recent['driving_type'].value_counts()
        axes[1, 1].pie(driving_dist.values, labels=driving_dist.index, autopct='%1.1f%%')
        axes[1, 1].set_title('Driving Type Distribution')
        
        # Consumption by driving type
        consumption_by_type = df_recent.groupby('driving_type')['actual_consumption_l_100km'].mean()
        axes[1, 2].bar(consumption_by_type.index, consumption_by_type.values, color=['blue', 'green', 'orange'])
        axes[1, 2].set_title('Average Consumption by Driving Type')
        axes[1, 2].set_ylabel('L/100km')
        
        plt.tight_layout()
        plt.show()
    
    def export_report(self, report, filename):
        """Export report to JSON file."""
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Report exported to {filename}")

def main_demo():
    """Demonstrate the updated fuel tracking system with ODO meter."""
    print("="*60)
    print("COMPREHENSIVE FUEL TRACKING AND ANALYSIS SYSTEM")
    print("WITH ODO METER INTEGRATION")
    print("="*60)
    
    # Initialize the tracker
    tracker = VehicleFuelTracker()
    
    # Add sample vehicle data
    vehicle_data = {
    'userid': '001',
    'vehicle_id': '01',
    'Make': 'BMW',
    'Model': 'X5',
    'Vehicle Class': 'SUV: SMALL',
    'Engine Size': '3.0 L',
    'Cylinders': 6,
    'Transmission': 'A8',
    'Fuel Type': 'X',
    'ODO_meter_when_buy_vehicle': 10000,  # REALISTIC STARTING POINT
    'full_tank_capacity': 83
}
    
    tracker.add_vehicle(vehicle_data)
    
    # Add sample fuel records with ODO meter readings
    fuel_records = [
    {
        'vehicle_id': '01',
        'time': '8:00am',
        'date': '2025-03-01',
        'existing_tank_percentage': 28,
        'after_refuel_percentage': 100,
        'ODO_meter_current_value': 10550,  # 550 km from initial 10000
        'driving_type': 'city',
        'location': 'Kandy',
        'fuel_price': 325
    },
    {
        'vehicle_id': '01',
        'time': '3:00pm',
        'date': '2025-03-08',
        'existing_tank_percentage': 22,
        'after_refuel_percentage': 100,
        'ODO_meter_current_value': 11230,  # 680 km from previous
        'driving_type': 'mix',
        'location': 'Colombo',
        'fuel_price': 330
    },
    {
        'vehicle_id': '01',
        'time': '10:00am',
        'date': '2025-03-15',
        'existing_tank_percentage': 25,
        'after_refuel_percentage': 100,
        'ODO_meter_current_value': 11920,  # 690 km from previous
        'driving_type': 'city',
        'location': 'Gampaha',
        'fuel_price': 328
    },
    {
        'vehicle_id': '01',
        'time': '5:30pm',
        'date': '2025-03-22',
        'existing_tank_percentage': 20,
        'after_refuel_percentage': 100,
        'ODO_meter_current_value': 12610,  # 690 km from previous
        'driving_type': 'mix',
        'location': 'Negombo',
        'fuel_price': 327
    },
    {
        'vehicle_id': '01',
        'time': '11:00am',
        'date': '2025-03-29',
        'existing_tank_percentage': 18,
        'after_refuel_percentage': 100,
        'ODO_meter_current_value': 13280,  # 670 km from previous
        'driving_type': 'city',
        'location': 'Kurunegala',
        'fuel_price': 329
    }
]

    
    for record in fuel_records:
        tracker.add_fuel_record(record)
    
    print("\n" + "="*50)
    print("SAMPLE REPORTS WITH ACCURATE KM CALCULATIONS")
    print("="*50)
    
    # Generate daily report
    print("\n1. DAILY REPORT")
    print("-" * 30)
    daily_report = tracker.generate_daily_report('01', '2025-03-01')
    for key, value in daily_report.items():
        if key != 'records':
            print(f"{key}: {value}")
    
    # Generate monthly report
    print("\n2. MONTHLY REPORT")
    print("-" * 30)
    monthly_report = tracker.generate_monthly_report('01', 2025, 3)
    for key, value in monthly_report.items():
        if key not in ['recommendations', 'driving_breakdown']:
            print(f"{key}: {value}")
    
    print(f"\nDriving Breakdown:")
    if 'driving_breakdown' in monthly_report:
        for driving_type, stats in monthly_report['driving_breakdown'].items():
            print(f"  {driving_type}: {stats}")
    
    # Generate yearly forecast
    print("\n3. YEARLY FORECAST")
    print("-" * 30)
    yearly_report = tracker.generate_yearly_forecast('01', 2025)
    for key, value in yearly_report.items():
        if key not in ['cost_optimization_tips', 'maintenance_recommendations', 'driving_pattern_analysis']:
            print(f"{key}: {value}")
    
    print(f"\nDriving Pattern Analysis:")
    if 'driving_pattern_analysis' in yearly_report:
        for pattern, stats in yearly_report['driving_pattern_analysis'].items():
            print(f"  {pattern}: {stats}")
    
    # Show AI recommendations
    print("\n4. AI RECOMMENDATIONS")
    print("-" * 30)
    print("Monthly Recommendations:")
    print(monthly_report.get('recommendations', 'Not available'))
    
    print("\nMaintenance Recommendations:")
    print(yearly_report.get('maintenance_recommendations', 'Not available'))
    
    # Create visualizations
    print("\n5. FUEL CONSUMPTION VISUALIZATIONS")
    print("-" * 30)
    tracker.visualize_fuel_trends('01', days=30)
    
    # Export reports
    tracker.export_report(monthly_report, 'monthly_fuel_report.json')
    tracker.export_report(yearly_report, 'yearly_fuel_report.json')
    
    print("\n" + "="*60)
    print("SYSTEM DEMONSTRATION COMPLETED")
    print("ACCURATE KM-BASED CALCULATIONS INTEGRATED")
    print("="*60)
    
    return tracker

if __name__ == "__main__":
    tracker = main_demo()