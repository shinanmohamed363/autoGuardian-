import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import json
from datetime import datetime, timedelta
import google.generativeai as genai
import warnings
from collections import defaultdict
import os
warnings.filterwarnings('ignore')

# Configure Google AI (replace with your actual API key)
genai.configure(api_key="AIzaSyCTSwSJgM3xfBNz2xcLHBhAb2Fn1YTl0So")

class IntegratedFuelSystem:
    """
    Integrated system that combines ML model predictions with real-world tracking
    """
    
    def __init__(self, model_path='model/enhanced_fuel_model.joblib'):
        self.model = None
        self.vehicles = {}
        self.fuel_records = []
        self.load_model(model_path)
        
        # Setup plotting style
        plt.style.use('default')
        sns.set_palette("husl")
        
        print("🚗 Integrated Fuel System Initialized")
        print("=" * 50)
    
    def load_model(self, model_path):
        """Load the trained ML model"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                print("✅ ML Model loaded successfully!")
            else:
                print("❌ Model not found. Please run the enhanced model training first.")
                print("   Note: System will work with limited functionality without ML model")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
    
    def add_vehicle(self, vehicle_data):
        """Add a vehicle to the system"""
        vehicle_id = vehicle_data['vehicle_id']
        self.vehicles[vehicle_id] = vehicle_data
        print(f"✅ Vehicle {vehicle_id} ({vehicle_data['Make']} {vehicle_data['Model']}) added")
        
        # Display vehicle specifications
        print(f"   📋 Specifications:")
        print(f"      Engine: {vehicle_data['Engine Size']} {vehicle_data['Cylinders']} cylinders")
        print(f"      Transmission: {vehicle_data['Transmission']}")
        print(f"      Fuel Type: {vehicle_data['Fuel Type']}")
        print(f"      Tank Capacity: {vehicle_data['full_tank_capacity']}L")
    
    def get_model_predictions(self, vehicle_id):
        """Get ML model predictions for a vehicle"""
        if not self.model or vehicle_id not in self.vehicles:
            return None
        
        vehicle = self.vehicles[vehicle_id]
        
        # Prepare input for ML model
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
            
            combined = predictions[0][0]
            emissions = predictions[0][1]
            
            return {
                'combined_l_100km': round(combined, 2),
                'highway_l_100km': round(combined * 0.85, 2),  # 15% better on highway
                'city_l_100km': round(combined * 1.20, 2),     # 20% worse in city
                'emissions_g_km': round(emissions, 2),
                'efficiency_rating': self._get_efficiency_rating(combined)
            }
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return None
    
    def _map_transmission(self, transmission_type):
        """Map transmission types to model format"""
        mapping = {
            'Automatic': 'A4',
            'Manual': 'M6', 
            'CVT': 'AV',
            'Semi-Automatic': 'AS',
            'A8': 'A8'  # Already in correct format
        }
        return mapping.get(transmission_type, 'A4')
    
    def _map_fuel_type(self, fuel_type):
        """Map fuel types to model format"""
        mapping = {
            'Regular Gasoline': 'X',
            'Premium Gasoline': 'Z',
            'Diesel': 'D',
            'Hybrid': 'X',
            'X': 'X',  # Already in correct format
            'Z': 'Z',
            'D': 'D'
        }
        return mapping.get(fuel_type, 'X')
    
    def _get_efficiency_rating(self, consumption):
        """Rate vehicle efficiency"""
        if consumption < 6:
            return "⭐⭐⭐⭐⭐ Excellent"
        elif consumption < 8:
            return "⭐⭐⭐⭐ Good"
        elif consumption < 10:
            return "⭐⭐⭐ Average"
        elif consumption < 12:
            return "⭐⭐ Below Average"
        else:
            return "⭐ Poor"
    
    def add_fuel_record(self, fuel_record):
        """Add a fuel refill record with ODO meter validation"""
        vehicle_id = fuel_record['vehicle_id']
        current_odo = fuel_record['ODO_meter_current_value']
        
        # Validate ODO meter reading
        vehicle_records = [r for r in self.fuel_records if r['vehicle_id'] == vehicle_id]
        if vehicle_records:
            last_odo = max([r['ODO_meter_current_value'] for r in vehicle_records])
            if current_odo < last_odo:
                print(f"⚠️  Warning: ODO meter reading ({current_odo}) is less than previous reading ({last_odo})")
                return False
        
        # Calculate actual fuel added based on tank percentages
        vehicle = self.vehicles[fuel_record['vehicle_id']]
        tank_capacity = vehicle['full_tank_capacity']
        
        fuel_percentage_added = fuel_record['after_refuel_percentage'] - fuel_record['existing_tank_percentage']
        actual_fuel_added = (fuel_percentage_added / 100) * tank_capacity
        
        fuel_record['calculated_fuel_added'] = round(actual_fuel_added, 2)
        fuel_record['total_cost'] = round(actual_fuel_added * fuel_record['fuel_price'] / 100, 2)
        
        # Calculate kilometers driven since last refuel
        if vehicle_records:
            previous_record = max(vehicle_records, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
            km_driven = current_odo - previous_record['ODO_meter_current_value']
            fuel_record['km_driven_since_last'] = km_driven
            
            # Calculate actual consumption rate
            if km_driven > 0:
                consumption_rate = (actual_fuel_added / km_driven) * 100
                fuel_record['actual_consumption_l_100km'] = round(consumption_rate, 2)
            else:
                fuel_record['actual_consumption_l_100km'] = 0
        else:
            # First record - calculate from initial ODO
            initial_odo = vehicle.get('ODO_meter_when_buy_vehicle', 0)
            km_driven = current_odo - initial_odo
            fuel_record['km_driven_since_last'] = km_driven
            
            if km_driven > 0:
                consumption_rate = (actual_fuel_added / km_driven) * 100
                fuel_record['actual_consumption_l_100km'] = round(consumption_rate, 2)
            else:
                fuel_record['actual_consumption_l_100km'] = 0
        
        self.fuel_records.append(fuel_record)
        print(f"✅ Fuel record added: {actual_fuel_added}L, {km_driven}km driven, ${fuel_record['total_cost']:.2f}")
        return True
    
    def generate_comprehensive_report(self, vehicle_id, period_days=30):
        """Generate a comprehensive analysis report"""
        print("\n" + "="*80)
        print(f"🚗 COMPREHENSIVE FUEL ANALYSIS REPORT - Vehicle {vehicle_id}")
        print("="*80)
        
        # Get ML model predictions
        predictions = self.get_model_predictions(vehicle_id)
        
        # Filter records for the period
        end_date = datetime.now()
        start_date = end_date - timedelta(days=period_days)
        
        period_records = [
            r for r in self.fuel_records 
            if r['vehicle_id'] == vehicle_id 
            and start_date <= datetime.strptime(r['date'], '%Y-%m-%d') <= end_date
        ]
        
        if not period_records:
            print(f"❌ No fuel records found for the period {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            return
        
        # Calculate actual consumption stats
        total_fuel = sum([r['calculated_fuel_added'] for r in period_records])
        total_cost = sum([r['total_cost'] for r in period_records])
        total_km = sum([r.get('km_driven_since_last', 0) for r in period_records])
        avg_price_per_liter = (total_cost / total_fuel) if total_fuel > 0 else 0
        actual_consumption = (total_fuel / total_km * 100) if total_km > 0 else 0
        
        # Analyze by driving type
        driving_stats = defaultdict(lambda: {'fuel': 0, 'cost': 0, 'count': 0, 'km': 0})
        for record in period_records:
            driving_type = record['driving_type']
            driving_stats[driving_type]['fuel'] += record['calculated_fuel_added']
            driving_stats[driving_type]['cost'] += record['total_cost']
            driving_stats[driving_type]['count'] += 1
            driving_stats[driving_type]['km'] += record.get('km_driven_since_last', 0)
        
        # Print report sections
        print(f"\n📅 PERIOD: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')} ({period_days} days)")
        print(f"🚙 VEHICLE: {self.vehicles[vehicle_id]['Make']} {self.vehicles[vehicle_id]['Model']}")
        
        if predictions:
            print(f"\n📊 ML MODEL PREDICTIONS:")
            print(f"   Combined Consumption: {predictions['combined_l_100km']} L/100km")
            print(f"   Highway Consumption:  {predictions['highway_l_100km']} L/100km") 
            print(f"   City Consumption:     {predictions['city_l_100km']} L/100km")
            print(f"   CO2 Emissions:        {predictions['emissions_g_km']} g/km")
            print(f"   Efficiency Rating:    {predictions['efficiency_rating']}")
        else:
            print("\n⚠️ ML model predictions unavailable")
        
        print(f"\n📈 ACTUAL CONSUMPTION DATA:")
        print(f"   Total Fuel Used:      {total_fuel:.2f} L")
        print(f"   Total Distance:       {total_km} km")
        print(f"   Actual Consumption:   {actual_consumption:.2f} L/100km")
        print(f"   Total Cost:           ${total_cost:.2f}")
        print(f"   Average Price/Liter:  ${avg_price_per_liter:.2f}")
        print(f"   Number of Refuels:    {len(period_records)}")
        
        print(f"\n🛣️  DRIVING PATTERN BREAKDOWN:")
        for driving_type, stats in driving_stats.items():
            fuel_pct = (stats['fuel'] / total_fuel) * 100 if total_fuel > 0 else 0
            km_pct = (stats['km'] / total_km) * 100 if total_km > 0 else 0
            type_consumption = (stats['fuel'] / stats['km'] * 100) if stats['km'] > 0 else 0
            print(f"   {driving_type.upper():<12}: {stats['fuel']:.1f}L ({fuel_pct:.1f}%), {stats['km']}km ({km_pct:.1f}%), {type_consumption:.2f}L/100km")
        
        # Performance comparison
        if predictions and total_km > 0:
            expected_consumption = predictions['combined_l_100km']
            performance_diff = actual_consumption - expected_consumption
            performance_pct = (performance_diff / expected_consumption) * 100
            
            print(f"\n⚡ PERFORMANCE ANALYSIS:")
            print(f"   Expected Consumption:  {expected_consumption:.2f} L/100km")
            print(f"   Actual Consumption:    {actual_consumption:.2f} L/100km")
            print(f"   Difference:            {performance_diff:+.2f} L/100km ({performance_pct:+.1f}%)")
            
            if performance_pct < -10:
                status = "🟢 EXCELLENT - Much better than expected!"
            elif performance_pct < 0:
                status = "🟡 GOOD - Better than expected"
            elif performance_pct < 10:
                status = "🟠 AVERAGE - Close to expected"
            else:
                status = "🔴 POOR - Much worse than expected"
            
            print(f"   Status: {status}")
        
        # Generate AI recommendations
        if predictions:
            ai_tips = self._get_ai_recommendations(predictions, dict(driving_stats), 
                                                 performance_pct if 'performance_pct' in locals() else 0, 
                                                 actual_consumption)
            print(f"\n🤖 AI-POWERED RECOMMENDATIONS:")
            print(ai_tips)
        
        # Create visualizations
        self._create_visualizations(vehicle_id, period_records, predictions, dict(driving_stats))
        
        # Monthly and yearly projections
        self._calculate_projections(total_fuel, total_cost, period_days, total_km, actual_consumption)
        
        return {
            'predictions': predictions,
            'actual_stats': {
                'total_fuel': total_fuel,
                'total_cost': total_cost,
                'total_km': total_km,
                'actual_consumption': actual_consumption
            },
            'driving_stats': dict(driving_stats),
            'performance': {
                'difference_consumption': performance_diff if 'performance_diff' in locals() else 0,
                'percentage_diff': performance_pct if 'performance_pct' in locals() else 0,
                'status': status if 'status' in locals() else "Unknown"
            }
        }
    
    def _get_ai_recommendations(self, predictions, driving_stats, performance_pct, actual_consumption):
        """Get AI-powered recommendations"""
        try:
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            prompt = f"""
            As a fuel efficiency expert, analyze this vehicle's performance and provide specific recommendations:
            
            Vehicle Performance:
            - Model predicted consumption: {predictions['combined_l_100km']} L/100km
            - Actual consumption: {actual_consumption:.2f} L/100km
            - Performance difference: {performance_pct:.1f}%
            - Driving pattern breakdown: {driving_stats}
            
            Please provide:
            1. 3 specific fuel-saving tips based on the data
            2. Driving behavior improvements for different driving types
            3. Maintenance recommendations (if consumption is high)
            4. Cost optimization strategies
            
            Keep recommendations practical and actionable. Format as numbered points.
            """
            
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"AI recommendations unavailable: {str(e)}"
    
    def _create_visualizations(self, vehicle_id, records, predictions, driving_stats):
        """Create comprehensive visualizations"""
        try:
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle(f'🚗 Fuel Analysis Dashboard - Vehicle {vehicle_id}', fontsize=16, fontweight='bold')
            
            # 1. Daily fuel consumption and km driven over time
            df = pd.DataFrame(records)
            df['date'] = pd.to_datetime(df['date'])
            daily_fuel = df.groupby('date')['calculated_fuel_added'].sum()
            daily_km = df.groupby('date')['km_driven_since_last'].sum()
            
            ax1 = axes[0, 0]
            ax1_twin = ax1.twinx()
            
            line1 = ax1.plot(daily_fuel.index, daily_fuel.values, 'b-o', label='Fuel (L)', linewidth=2, markersize=6)
            line2 = ax1_twin.plot(daily_km.index, daily_km.values, 'r-s', label='Distance (km)', linewidth=2, markersize=6)
            
            ax1.set_xlabel('Date')
            ax1.set_ylabel('Fuel Added (L)', color='b')
            ax1_twin.set_ylabel('Distance Driven (km)', color='r')
            ax1.set_title('📈 Daily Fuel Consumption & Distance', fontweight='bold')
            ax1.grid(True, alpha=0.3)
            
            # Combine legends
            lines = line1 + line2
            labels = [l.get_label() for l in lines]
            ax1.legend(lines, labels, loc='upper left')
            
            # 2. Driving type distribution (fuel consumption)
            if driving_stats:
                types = list(driving_stats.keys())
                fuel_amounts = [driving_stats[t]['fuel'] for t in types]
                colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']
                
                wedges, texts, autotexts = axes[0, 1].pie(fuel_amounts, labels=types, autopct='%1.1f%%', 
                                                         colors=colors[:len(types)], startangle=90)
                axes[0, 1].set_title('🛣️ Fuel Consumption by Driving Type', fontweight='bold')
                
                # Make percentage text bold
                for autotext in autotexts:
                    autotext.set_fontweight('bold')
                    autotext.set_color('white')
            
            # 3. Daily costs and consumption rate
            daily_cost = df.groupby('date')['total_cost'].sum()
            daily_consumption = (daily_fuel / daily_km * 100).dropna()
            
            ax3 = axes[1, 0]
            ax3_twin = ax3.twinx()
            
            bars = ax3.bar(range(len(daily_cost)), daily_cost.values, color='#E74C3C', alpha=0.7, label='Cost ($)')
            if len(daily_consumption) > 0:
                line3 = ax3_twin.plot(range(len(daily_consumption)), daily_consumption.values, 'g-o', 
                                     linewidth=2, markersize=6, label='L/100km')
            
            ax3.set_title('💰 Daily Costs & Consumption Rate', fontweight='bold')
            ax3.set_xlabel('Days')
            ax3.set_ylabel('Cost ($)', color='r')
            ax3_twin.set_ylabel('Consumption (L/100km)', color='g')
            ax3.grid(True, alpha=0.3)
            
            # 4. Model vs Actual comparison (if predictions available)
            if predictions:
                categories = ['Highway', 'City', 'Combined']
                model_values = [predictions['highway_l_100km'], predictions['city_l_100km'], predictions['combined_l_100km']]
                
                # Calculate actual consumption by type if available
                actual_values = []
                for cat in ['highway', 'city', 'mix']:
                    if cat in driving_stats and driving_stats[cat]['km'] > 0:
                        actual_consumption = (driving_stats[cat]['fuel'] / driving_stats[cat]['km']) * 100
                        actual_values.append(actual_consumption)
                    else:
                        actual_values.append(0)
                
                x = np.arange(len(categories))
                width = 0.35
                
                bars1 = axes[1, 1].bar(x - width/2, model_values, width, label='Model Prediction', 
                                      color='#3498DB', alpha=0.8)
                bars2 = axes[1, 1].bar(x + width/2, actual_values, width, label='Actual (if available)', 
                                      color='#E74C3C', alpha=0.8)
                
                axes[1, 1].set_title('📊 Model vs Actual Consumption', fontweight='bold')
                axes[1, 1].set_ylabel('L/100km')
                axes[1, 1].set_xticks(x)
                axes[1, 1].set_xticklabels(categories)
                axes[1, 1].legend()
                axes[1, 1].grid(True, alpha=0.3)
                
                # Add value labels on bars
                for bars in [bars1, bars2]:
                    for bar in bars:
                        height = bar.get_height()
                        if height > 0:
                            axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + 0.1,
                                           f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"❌ Visualization error: {e}")
    
    def _calculate_projections(self, total_fuel, total_cost, period_days, total_km, actual_consumption):
        """Calculate monthly and yearly projections"""
        print(f"\n📅 PROJECTIONS:")
        
        daily_avg_fuel = total_fuel / period_days if period_days > 0 else 0
        daily_avg_cost = total_cost / period_days if period_days > 0 else 0
        daily_avg_km = total_km / period_days if period_days > 0 else 0
        
        # Monthly projections
        monthly_fuel = daily_avg_fuel * 30
        monthly_cost = daily_avg_cost * 30
        monthly_km = daily_avg_km * 30
        
        print(f"   📊 MONTHLY PROJECTION (30 days):")
        print(f"      Fuel Consumption: {monthly_fuel:.1f} L")
        print(f"      Estimated Cost:   ${monthly_cost:.2f}")
        print(f"      Distance Driven:  {monthly_km:.0f} km")
        print(f"      Avg Consumption:  {actual_consumption:.2f} L/100km")
        
        # Yearly projections
        yearly_fuel = daily_avg_fuel * 365
        yearly_cost = daily_avg_cost * 365
        yearly_km = daily_avg_km * 365
        yearly_emissions = yearly_fuel * 2.31  # CO2 emission factor for gasoline
        
        print(f"   📊 YEARLY PROJECTION (365 days):")
        print(f"      Fuel Consumption: {yearly_fuel:.1f} L")
        print(f"      Estimated Cost:   ${yearly_cost:.2f}")
        print(f"      Distance Driven:  {yearly_km:.0f} km")
        print(f"      CO2 Emissions:    {yearly_emissions:.1f} kg")
        
        # Environmental impact
        trees_needed = yearly_emissions / 22  # One tree absorbs ~22kg CO2 per year
        print(f"      Trees needed to offset: {trees_needed:.0f} trees")
    
    def compare_vehicles(self, vehicle_ids, period_days=30):
        """Compare multiple vehicles' performance"""
        print("\n" + "="*80)
        print("🏁 VEHICLE COMPARISON ANALYSIS")
        print("="*80)
        
        comparison_data = []
        
        for vehicle_id in vehicle_ids:
            if vehicle_id not in self.vehicles:
                continue
                
            # Get vehicle data
            vehicle = self.vehicles[vehicle_id]
            predictions = self.get_model_predictions(vehicle_id)
            
            # Filter records for the period
            end_date = datetime.now()
            start_date = end_date - timedelta(days=period_days)
            
            period_records = [
                r for r in self.fuel_records 
                if r['vehicle_id'] == vehicle_id 
                and start_date <= datetime.strptime(r['date'], '%Y-%m-%d') <= end_date
            ]
            
            if not period_records:
                continue
                
            total_fuel = sum([r['calculated_fuel_added'] for r in period_records])
            total_cost = sum([r['total_cost'] for r in period_records])
            total_km = sum([r.get('km_driven_since_last', 0) for r in period_records])
            actual_consumption = (total_fuel / total_km * 100) if total_km > 0 else 0
            
            comparison_data.append({
                'vehicle_id': vehicle_id,
                'make_model': f"{vehicle['Make']} {vehicle['Model']}",
                'predicted_consumption': predictions['combined_l_100km'] if predictions else 'N/A',
                'actual_consumption': actual_consumption,
                'total_fuel': total_fuel,
                'total_cost': total_cost,
                'total_km': total_km,
                'avg_cost_per_km': total_cost / total_km if total_km > 0 else 0
            })
        
        if not comparison_data:
            print("❌ No data available for comparison")
            return
        
        # Sort by actual consumption (most efficient first)
        comparison_data.sort(key=lambda x: x['actual_consumption'])
        
        print(f"\n📊 EFFICIENCY RANKING (Best to Worst):")
        print("-" * 80)
        for i, data in enumerate(comparison_data, 1):
            print(f"{i}. {data['make_model']} (ID: {data['vehicle_id']})")
            print(f"   Actual: {data['actual_consumption']:.2f} L/100km | "
                  f"Predicted: {data['predicted_consumption']} L/100km")
            print(f"   Total: {data['total_fuel']:.1f}L, {data['total_km']}km, ${data['total_cost']:.2f}")
            print(f"   Cost per km: ${data['avg_cost_per_km']:.3f}")
            print()
        
        return comparison_data
    
    def export_comprehensive_data(self, filename="fuel_analysis_export.json"):
        """Export all data for external analysis"""
        export_data = {
            'vehicles': self.vehicles,
            'fuel_records': self.fuel_records,
            'export_timestamp': datetime.now().isoformat(),
            'summary_stats': self._calculate_summary_stats()
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"✅ Comprehensive data exported to {filename}")
    
    def _calculate_summary_stats(self):
        """Calculate overall system statistics"""
        if not self.fuel_records:
            return {}
        
        total_fuel = sum([r['calculated_fuel_added'] for r in self.fuel_records])
        total_cost = sum([r['total_cost'] for r in self.fuel_records])
        total_km = sum([r.get('km_driven_since_last', 0) for r in self.fuel_records])
        
        return {
            'total_vehicles': len(self.vehicles),
            'total_records': len(self.fuel_records),
            'total_fuel_consumed': total_fuel,
            'total_money_spent': total_cost,
            'total_distance_driven': total_km,
            'overall_consumption': (total_fuel / total_km * 100) if total_km > 0 else 0,
            'average_fuel_price': total_cost / total_fuel if total_fuel > 0 else 0
        }


def demo_integrated_system():
    """Demonstrate the integrated fuel system"""
    print("🚀 STARTING INTEGRATED FUEL SYSTEM DEMO")
    print("="*60)
    
    # Initialize system
    system = IntegratedFuelSystem()
    
    # Add sample vehicles
    vehicles = [
        {
            'userid': '001',
            'vehicle_id': 'BMW_01',
            'Make': 'BMW',
            'Model': 'X5',
            'Vehicle Class': 'SUV: SMALL',
            'Engine Size': '3.0 L',
            'Cylinders': 6,
            'Transmission': 'A8',
            'Fuel Type': 'Z',
            'ODO_meter_when_buy_vehicle': 10000,
            'full_tank_capacity': 83
        },
        {
            'userid': '002',
            'vehicle_id': 'TOYOTA_01',
            'Make': 'TOYOTA',
            'Model': 'CAMRY',
            'Vehicle Class': 'COMPACT',
            'Engine Size': '2.5 L',
            'Cylinders': 4,
            'Transmission': 'A6',
            'Fuel Type': 'X',
            'ODO_meter_when_buy_vehicle': 5000,
            'full_tank_capacity': 60
        }
    ]
    
    for vehicle in vehicles:
        system.add_vehicle(vehicle)
        print()
    
    # Add sample fuel records with updated dates
    fuel_records = [
        # BMW Records (updated dates)
        {
            'vehicle_id': 'BMW_01',
            'time': '8:00am',
            'date': '2025-05-01',
            'existing_tank_percentage': 25,
            'after_refuel_percentage': 100,
            'ODO_meter_current_value': 10650,
            'driving_type': 'city',
            'location': 'Colombo',
            'fuel_price': 340
        },
        {
            'vehicle_id': 'BMW_01',
            'time': '3:00pm',
            'date': '2025-05-08',
            'existing_tank_percentage': 20,
            'after_refuel_percentage': 100,
            'ODO_meter_current_value': 11200,
            'driving_type': 'highway',
            'location': 'Kandy',
            'fuel_price': 330
        },
        {
            'vehicle_id': 'BMW_01',
            'time': '11:00am',
            'date': '2025-05-15',
            'existing_tank_percentage': 30,
            'after_refuel_percentage': 100,
            'ODO_meter_current_value': 11800,
            'driving_type': 'mix',
            'location': 'Galle',
            'fuel_price': 350
        },
        # Toyota Records (updated dates)
        {
            'vehicle_id': 'TOYOTA_01',
            'time': '9:30am',
            'date': '2025-05-02',
            'existing_tank_percentage': 20,
            'after_refuel_percentage': 100,
            'ODO_meter_current_value': 5500,
            'driving_type': 'city',
            'location': 'Colombo',
            'fuel_price': 320
        },
        {
            'vehicle_id': 'TOYOTA_01',
            'time': '2:00pm',
            'date': '2025-05-10',
            'existing_tank_percentage': 25,
            'after_refuel_percentage': 100,
            'ODO_meter_current_value': 6200,
            'driving_type': 'highway',
            'location': 'Jaffna',
            'fuel_price': 310
        },
        {
            'vehicle_id': 'TOYOTA_01',
            'time': '10:00am',
            'date': '2025-05-18',
            'existing_tank_percentage': 15,
            'after_refuel_percentage': 100,
            'ODO_meter_current_value': 7000,
            'driving_type': 'city',
            'location': 'Colombo',
            'fuel_price': 325
        }
    ]
    
    print("\n⛽ ADDING FUEL RECORDS...")
    for record in fuel_records:
        system.add_fuel_record(record)
        print()
    
    # Generate comprehensive report for BMW
    print("\n📊 GENERATING REPORT FOR BMW...")
    system.generate_comprehensive_report('BMW_01')
    
    # Generate comprehensive report for Toyota
    print("\n📊 GENERATING REPORT FOR TOYOTA...")
    system.generate_comprehensive_report('TOYOTA_01')
    
    # Compare both vehicles
    print("\n🏁 COMPARING VEHICLES...")
    system.compare_vehicles(['BMW_01', 'TOYOTA_01'])
    
    # Export data
    system.export_comprehensive_data()
    
    print("\n✅ DEMO COMPLETED SUCCESSFULLY!")


if __name__ == "__main__":
    demo_integrated_system()