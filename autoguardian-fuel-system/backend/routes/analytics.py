"""
AutoGuardian Fuel Management System - Analytics Routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date, timedelta
from collections import defaultdict

from database import db
from models.vehicle import Vehicle, VehicleStatistics
from models.fuel_record import FuelRecord
from models.predictions import MLPrediction
from models.user import User
from utils.validators import validate_date_range, validate_required_fields

# Create analytics blueprint
analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/comprehensive-report/<vehicle_id>', methods=['POST'])
@jwt_required()
def generate_comprehensive_report(vehicle_id):
    """Generate comprehensive analysis report for a vehicle"""
    try:
        current_user_id = get_jwt_identity()
        
        # Check if user owns the vehicle
        vehicle = Vehicle.find_by_id(vehicle_id)
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        
        if vehicle.user_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json() or {}
        period_days = data.get('period_days', 30)
        
        # Calculate date range
        end_date = date.today()
        start_date = end_date - timedelta(days=period_days)
        
        # Get fuel records for the period
        fuel_records = FuelRecord.query.filter(
            FuelRecord.vehicle_id == vehicle_id,
            FuelRecord.record_date >= start_date,
            FuelRecord.record_date <= end_date
        ).order_by(FuelRecord.record_date.desc()).all()
        
        if not fuel_records:
            return jsonify({
                'error': 'No fuel records found for the specified period',
                'period': f"{start_date} to {end_date}"
            }), 404
        
        # Get latest ML prediction
        prediction = MLPrediction.get_latest_prediction(vehicle_id)
        
        # Calculate actual consumption stats
        total_fuel = sum(float(r.calculated_fuel_added) for r in fuel_records)
        total_cost = sum(float(r.total_cost) for r in fuel_records)
        total_km = sum(r.km_driven_since_last for r in fuel_records)
        actual_consumption = (total_fuel / total_km * 100) if total_km > 0 else 0
        avg_price_per_liter = (total_cost / total_fuel) if total_fuel > 0 else 0
        
        # Analyze by driving type
        driving_stats = defaultdict(lambda: {'fuel': 0, 'cost': 0, 'count': 0, 'km': 0})
        for record in fuel_records:
            dtype = record.driving_type
            driving_stats[dtype]['fuel'] += float(record.calculated_fuel_added)
            driving_stats[dtype]['cost'] += float(record.total_cost)
            driving_stats[dtype]['count'] += 1
            driving_stats[dtype]['km'] += record.km_driven_since_last
        
        # Calculate consumption by driving type
        for dtype_data in driving_stats.values():
            if dtype_data['km'] > 0:
                dtype_data['consumption'] = (dtype_data['fuel'] / dtype_data['km']) * 100
            else:
                dtype_data['consumption'] = 0
        
        # Performance comparison with ML prediction
        performance_analysis = None
        if prediction and total_km > 0:
            expected_consumption = float(prediction.combined_l_100km)
            performance_diff = actual_consumption - expected_consumption
            performance_pct = (performance_diff / expected_consumption) * 100
            
            if performance_pct < -10:
                status = "Excellent - Much better than expected"
            elif performance_pct < 0:
                status = "Good - Better than expected"
            elif performance_pct < 10:
                status = "Average - Close to expected"
            else:
                status = "Poor - Much worse than expected"
            
            performance_analysis = {
                'expected_consumption': expected_consumption,
                'actual_consumption': round(actual_consumption, 2),
                'difference_l_100km': round(performance_diff, 2),
                'percentage_difference': round(performance_pct, 1),
                'status': status
            }
        
        # Calculate projections
        daily_avg_fuel = total_fuel / period_days if period_days > 0 else 0
        daily_avg_cost = total_cost / period_days if period_days > 0 else 0
        daily_avg_km = total_km / period_days if period_days > 0 else 0
        
        projections = {
            'monthly': {
                'fuel_consumption': round(daily_avg_fuel * 30, 1),
                'estimated_cost': round(daily_avg_cost * 30, 2),
                'distance_driven': round(daily_avg_km * 30),
                'avg_consumption': round(actual_consumption, 2)
            },
            'yearly': {
                'fuel_consumption': round(daily_avg_fuel * 365, 1),
                'estimated_cost': round(daily_avg_cost * 365, 2),
                'distance_driven': round(daily_avg_km * 365),
                'co2_emissions': round(daily_avg_fuel * 365 * 2.31, 1),  # kg CO2
                'trees_to_offset': round((daily_avg_fuel * 365 * 2.31) / 22)  # trees needed
            }
        }
        
        # Compile comprehensive report
        report = {
            'vehicle_info': {
                'vehicle_id': vehicle_id,
                'display_name': vehicle.display_name,
                'make': vehicle.make,
                'model': vehicle.model,
                'year': vehicle.year,
                'engine_info': vehicle.engine_info
            },
            'period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'days': period_days
            },
            'ml_prediction': prediction.to_dict() if prediction else None,
            'actual_data': {
                'total_fuel_used': round(total_fuel, 2),
                'total_distance': total_km,
                'actual_consumption': round(actual_consumption, 2),
                'total_cost': round(total_cost, 2),
                'average_price_per_liter': round(avg_price_per_liter, 2),
                'number_of_refuels': len(fuel_records)
            },
            'driving_patterns': dict(driving_stats),
            'performance_analysis': performance_analysis,
            'projections': projections,
            'fuel_records': [record.to_dict() for record in fuel_records[:10]]  # Latest 10 records
        }
        
        return jsonify({
            'report': report,
            'generated_at': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Report generation failed', 'message': str(e)}), 500

@analytics_bp.route('/driving-patterns/<vehicle_id>', methods=['GET'])
@jwt_required()
def get_driving_patterns(vehicle_id):
    """Get driving pattern analysis for a vehicle"""
    try:
        current_user_id = get_jwt_identity()
        
        # Check if user owns the vehicle
        vehicle = Vehicle.find_by_id(vehicle_id)
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        
        if vehicle.user_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Get query parameters
        days = request.args.get('days', 90, type=int)
        
        # Get driving pattern data
        patterns = vehicle.get_consumption_by_driving_type()
        
        # Calculate additional insights - ensure all values are converted to appropriate types
        total_fuel = sum(float(p['total_fuel']) if p['total_fuel'] is not None else 0.0 for p in patterns.values())
        total_km = sum(int(p['total_km']) if p['total_km'] is not None else 0 for p in patterns.values())
        
        pattern_analysis = {}
        for dtype, data in patterns.items():
            if total_fuel > 0 and total_km > 0:
                fuel_percentage = (float(data['total_fuel']) / total_fuel) * 100
                km_percentage = (data['total_km'] / total_km) * 100
                
                pattern_analysis[dtype] = {
                    'count': data['count'],
                    'total_fuel': float(data['total_fuel']),
                    'total_km': data['total_km'],
                    'avg_consumption': float(data['avg_consumption']),
                    'fuel_percentage': round(fuel_percentage, 1),
                    'km_percentage': round(km_percentage, 1),
                    'efficiency_rating': 'Good' if float(data['avg_consumption']) < 8 else 'Average' if float(data['avg_consumption']) < 12 else 'Poor'
                }
        
        return jsonify({
            'vehicle_id': vehicle_id,
            'driving_patterns': pattern_analysis,
            'summary': {
                'total_fuel': round(total_fuel, 2),
                'total_km': total_km,
                'overall_consumption': round((total_fuel / total_km * 100), 2) if total_km > 0 else 0,
                'most_efficient_type': min(patterns.keys(), key=lambda k: float(patterns[k]['avg_consumption'])) if patterns else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get driving patterns', 'message': str(e)}), 500

@analytics_bp.route('/consumption-trends/<vehicle_id>', methods=['GET'])
@jwt_required()
def get_consumption_trends(vehicle_id):
    """Get fuel consumption trends over time"""
    try:
        current_user_id = get_jwt_identity()
        
        # Check if user owns the vehicle
        vehicle = Vehicle.find_by_id(vehicle_id)
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        
        if vehicle.user_id != current_user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Get query parameters
        days = request.args.get('days', 180, type=int)
        
        # Get fuel records for trend analysis
        cutoff_date = date.today() - timedelta(days=days)
        records = FuelRecord.query.filter(
            FuelRecord.vehicle_id == vehicle_id,
            FuelRecord.record_date >= cutoff_date,
            FuelRecord.actual_consumption_l_100km > 0
        ).order_by(FuelRecord.record_date).all()
        
        if not records:
            return jsonify({
                'error': 'Insufficient data for trend analysis',
                'message': f'No records found in the last {days} days'
            }), 404
        
        # Group by month for trend analysis
        monthly_data = defaultdict(lambda: {'consumption': [], 'cost': [], 'dates': []})
        
        for record in records:
            month_key = record.record_date.strftime('%Y-%m')
            monthly_data[month_key]['consumption'].append(float(record.actual_consumption_l_100km))
            monthly_data[month_key]['cost'].append(float(record.total_cost))
            monthly_data[month_key]['dates'].append(record.record_date.isoformat())
        
        # Calculate monthly averages and trends
        trend_data = []
        for month, data in sorted(monthly_data.items()):
            avg_consumption = sum(data['consumption']) / len(data['consumption'])
            avg_cost = sum(data['cost']) / len(data['cost'])
            
            trend_data.append({
                'month': month,
                'avg_consumption': round(avg_consumption, 2),
                'avg_cost': round(avg_cost, 2),
                'record_count': len(data['consumption']),
                'min_consumption': round(min(data['consumption']), 2),
                'max_consumption': round(max(data['consumption']), 2)
            })
        
        # Calculate overall trend
        if len(trend_data) >= 3:
            recent_avg = sum(t['avg_consumption'] for t in trend_data[-3:]) / 3
            older_avg = sum(t['avg_consumption'] for t in trend_data[:3]) / 3
            
            if recent_avg < older_avg * 0.95:
                trend_direction = 'improving'
            elif recent_avg > older_avg * 1.05:
                trend_direction = 'declining'
            else:
                trend_direction = 'stable'
        else:
            trend_direction = 'insufficient_data'
        
        return jsonify({
            'vehicle_id': vehicle_id,
            'period_days': days,
            'trend_data': trend_data,
            'trend_analysis': {
                'direction': trend_direction,
                'total_records': len(records),
                'date_range': {
                    'start': records[0].record_date.isoformat(),
                    'end': records[-1].record_date.isoformat()
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get consumption trends', 'message': str(e)}), 500

@analytics_bp.route('/compare-vehicles', methods=['POST'])
@jwt_required()
def compare_vehicles():
    """Compare multiple vehicles' performance"""
    try:
        current_user_id = get_jwt_identity()
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        required_fields = ['vehicle_ids']
        missing_fields = validate_required_fields(data, required_fields)
        if missing_fields:
            return jsonify({'error': 'Missing required fields', 'missing_fields': missing_fields}), 400
        
        vehicle_ids = data['vehicle_ids']
        if not isinstance(vehicle_ids, list) or len(vehicle_ids) < 2:
            return jsonify({'error': 'At least 2 vehicle IDs required for comparison'}), 400
        
        if len(vehicle_ids) > 5:
            return jsonify({'error': 'Maximum 5 vehicles allowed for comparison'}), 400
        
        period_days = data.get('period_days', 30)
        
        # Get comparison data for each vehicle
        comparison_data = []
        
        for vehicle_id in vehicle_ids:
            # Check if user owns the vehicle
            vehicle = Vehicle.find_by_id(vehicle_id)
            if not vehicle or vehicle.user_id != current_user_id:
                continue
            
            # Get vehicle statistics
            stats = VehicleStatistics.get_or_create(vehicle_id)
            
            # Get recent fuel records
            cutoff_date = date.today() - timedelta(days=period_days)
            recent_records = FuelRecord.query.filter(
                FuelRecord.vehicle_id == vehicle_id,
                FuelRecord.record_date >= cutoff_date
            ).all()
            
            if recent_records:
                recent_fuel = sum(float(r.calculated_fuel_added) for r in recent_records)
                recent_cost = sum(float(r.total_cost) for r in recent_records)
                recent_km = sum(r.km_driven_since_last for r in recent_records)
                recent_consumption = (recent_fuel / recent_km * 100) if recent_km > 0 else 0
            else:
                recent_fuel = recent_cost = recent_km = recent_consumption = 0
            
            # Get ML prediction
            prediction = MLPrediction.get_latest_prediction(vehicle_id)
            
            comparison_data.append({
                'vehicle_id': vehicle_id,
                'vehicle_info': {
                    'make': vehicle.make,
                    'model': vehicle.model,
                    'year': vehicle.year,
                    'display_name': vehicle.display_name,
                    'engine_info': vehicle.engine_info
                },
                'predicted_consumption': float(prediction.combined_l_100km) if prediction else None,
                'recent_actual_consumption': round(recent_consumption, 2),
                'recent_total_fuel': round(recent_fuel, 2),
                'recent_total_cost': round(recent_cost, 2),
                'recent_total_km': recent_km,
                'cost_per_km': round(recent_cost / recent_km, 3) if recent_km > 0 else 0,
                'overall_stats': stats.to_dict()
            })
        
        # Sort by efficiency (lowest consumption first)
        comparison_data.sort(key=lambda x: x['recent_actual_consumption'] or 999)
        
        # Add rankings
        for i, vehicle_data in enumerate(comparison_data, 1):
            vehicle_data['efficiency_rank'] = i
        
        # Calculate comparison insights
        if len(comparison_data) >= 2:
            consumptions = [v['recent_actual_consumption'] for v in comparison_data if v['recent_actual_consumption'] > 0]
            costs = [v['recent_total_cost'] for v in comparison_data if v['recent_total_cost'] > 0]
            
            insights = {
                'most_efficient': comparison_data[0]['vehicle_info']['display_name'],
                'least_efficient': comparison_data[-1]['vehicle_info']['display_name'],
                'avg_consumption': round(sum(consumptions) / len(consumptions), 2) if consumptions else 0,
                'avg_cost': round(sum(costs) / len(costs), 2) if costs else 0,
                'consumption_range': {
                    'min': min(consumptions) if consumptions else 0,
                    'max': max(consumptions) if consumptions else 0
                }
            }
        else:
            insights = {}
        
        return jsonify({
            'comparison_data': comparison_data,
            'period_days': period_days,
            'insights': insights,
            'generated_at': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Vehicle comparison failed', 'message': str(e)}), 500

@analytics_bp.route('/dashboard/<int:user_id>', methods=['GET'])
@jwt_required()
def get_dashboard_data(user_id):
    """Get dashboard data for a user"""
    try:
        current_user_id = get_jwt_identity()
        
        # Users can only access their own dashboard
        if current_user_id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get user's vehicles
        vehicles = Vehicle.find_by_user(user_id)
        
        dashboard_data = {
            'user_info': user.to_dict(),
            'fleet_summary': {
                'total_vehicles': len(vehicles),
                'active_vehicles': len([v for v in vehicles if v.is_active])
            },
            'vehicles': [],
            'recent_activity': []
        }
        
        total_fuel = total_cost = total_km = 0
        
        for vehicle in vehicles[:5]:  # Limit to 5 vehicles for dashboard
            # Get vehicle stats
            stats = VehicleStatistics.get_or_create(vehicle.vehicle_id)
            
            # Get latest fuel record
            latest_record = vehicle.latest_fuel_record
            
            # Get latest prediction
            prediction = MLPrediction.get_latest_prediction(vehicle.vehicle_id)
            
            vehicle_data = {
                'vehicle_id': vehicle.vehicle_id,
                'display_name': vehicle.display_name,
                'engine_info': vehicle.engine_info,
                'latest_record': latest_record.to_dict() if latest_record else None,
                'prediction': prediction.to_dict(include_analysis=False) if prediction else None,
                'statistics': stats.to_dict()
            }
            
            dashboard_data['vehicles'].append(vehicle_data)
            
            # Add to totals
            total_fuel += float(stats.total_fuel_consumed)
            total_cost += float(stats.total_cost)
            total_km += stats.total_distance_driven
        
        # Fleet totals
        dashboard_data['fleet_summary'].update({
            'total_fuel_consumed': round(total_fuel, 2),
            'total_cost': round(total_cost, 2),
            'total_distance': total_km,
            'average_consumption': round((total_fuel / total_km * 100), 2) if total_km > 0 else 0
        })
        
        return jsonify(dashboard_data), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get dashboard data', 'message': str(e)}), 500