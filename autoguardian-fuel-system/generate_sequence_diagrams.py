#!/usr/bin/env python3
"""
AutoGuardian Fuel Management System - Sequence Diagram Generator
This script generates UML sequence diagrams showing key user flows and system interactions.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Arrow
import numpy as np

def create_user_login_sequence():
    """Generate sequence diagram for user login flow"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(8, 9.5, 'AutoGuardian - User Login Sequence', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    ax.text(8, 9.2, 'User Authentication Flow', 
            ha='center', va='center', fontsize=12, style='italic')
    
    # Define actors and objects
    actors = {
        'User': 2,
        'LoginPage': 4.5,
        'AuthService': 7,
        'Backend API': 9.5,
        'Database': 12,
        'JWT Service': 14
    }
    
    # Draw actor boxes and lifelines
    y_top = 8.5
    y_bottom = 1
    
    for actor, x_pos in actors.items():
        # Actor box
        box = FancyBboxPatch((x_pos-0.6, y_top-0.2), 1.2, 0.4,
                            boxstyle="round,pad=0.02", 
                            facecolor='#3B82F6', alpha=0.8, 
                            edgecolor='black', linewidth=1)
        ax.add_patch(box)
        ax.text(x_pos, y_top, actor, ha='center', va='center', 
                fontsize=9, color='white', fontweight='bold')
        
        # Lifeline (vertical dashed line)
        ax.plot([x_pos, x_pos], [y_top-0.2, y_bottom], 
                linestyle='--', color='gray', alpha=0.7, linewidth=1)
    
    # Define sequence steps
    sequences = [
        # (from_actor, to_actor, message, y_pos, message_type, return_message)
        ('User', 'LoginPage', '1: Enter credentials', 7.8, 'sync', None),
        ('LoginPage', 'AuthService', '2: login(email, password)', 7.4, 'async', None),
        ('AuthService', 'Backend API', '3: POST /api/auth/login', 7.0, 'async', None),
        ('Backend API', 'Database', '4: findUserByEmail(email)', 6.6, 'sync', None),
        ('Database', 'Backend API', '5: return User object', 6.3, 'return', None),
        ('Backend API', 'Backend API', '6: validatePassword(password)', 5.9, 'self', None),
        ('Backend API', 'JWT Service', '7: generateTokens(user)', 5.5, 'sync', None),
        ('JWT Service', 'Backend API', '8: return {access_token, refresh_token}', 5.2, 'return', None),
        ('Backend API', 'AuthService', '9: return AuthResponse', 4.8, 'return', None),
        ('AuthService', 'AuthService', '10: storeTokens(tokens)', 4.4, 'self', None),
        ('AuthService', 'LoginPage', '11: return success', 4.0, 'return', None),
        ('LoginPage', 'User', '12: redirect to Dashboard', 3.6, 'async', None),
    ]
    
    draw_sequence_messages(ax, actors, sequences)
    
    # Add notes
    note_box = Rectangle((0.5, 1.5), 3, 1.5, facecolor='#FEF3C7', alpha=0.8, edgecolor='#F59E0B')
    ax.add_patch(note_box)
    ax.text(2, 2.6, 'Notes:', ha='center', fontweight='bold', fontsize=10)
    ax.text(2, 2.3, '• Passwords are hashed using bcrypt', ha='center', fontsize=8)
    ax.text(2, 2.1, '• JWT tokens stored in localStorage', ha='center', fontsize=8)
    ax.text(2, 1.9, '• Failed login shows error message', ha='center', fontsize=8)
    ax.text(2, 1.7, '• Tokens have expiration times', ha='center', fontsize=8)
    
    plt.tight_layout()
    return fig

def create_fuel_record_sequence():
    """Generate sequence diagram for adding fuel record"""
    
    fig, ax = plt.subplots(1, 1, figsize=(18, 12))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Title
    ax.text(9, 11.5, 'AutoGuardian - Add Fuel Record Sequence', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    ax.text(9, 11.2, 'Fuel Record Creation with ML Prediction & AI Recommendations', 
            ha='center', va='center', fontsize=12, style='italic')
    
    # Define actors
    actors = {
        'User': 1.5,
        'FuelRecordsPage': 3.5,
        'ApiService': 5.5,
        'Backend API': 7.5,
        'FuelRecord Model': 9.5,
        'ML Service': 11.5,
        'AI Service': 13.5,
        'Database': 15.5,
        'Recommendation': 17
    }
    
    # Draw actor boxes and lifelines
    y_top = 10.5
    y_bottom = 1
    
    for actor, x_pos in actors.items():
        box = FancyBboxPatch((x_pos-0.6, y_top-0.2), 1.2, 0.4,
                            boxstyle="round,pad=0.02", 
                            facecolor='#10B981', alpha=0.8, 
                            edgecolor='black', linewidth=1)
        ax.add_patch(box)
        ax.text(x_pos, y_top, actor, ha='center', va='center', 
                fontsize=8, color='white', fontweight='bold')
        
        # Lifeline
        ax.plot([x_pos, x_pos], [y_top-0.2, y_bottom], 
                linestyle='--', color='gray', alpha=0.7, linewidth=1)
    
    # Define sequence steps
    sequences = [
        ('User', 'FuelRecordsPage', '1: Fill fuel record form', 9.8, 'sync', None),
        ('User', 'FuelRecordsPage', '2: Click "Add Record"', 9.5, 'sync', None),
        ('FuelRecordsPage', 'ApiService', '3: addFuelRecord(recordData)', 9.2, 'async', None),
        ('ApiService', 'Backend API', '4: POST /api/fuel-records', 8.9, 'async', None),
        ('Backend API', 'FuelRecord Model', '5: validate input data', 8.6, 'sync', None),
        ('FuelRecord Model', 'Backend API', '6: validation result', 8.3, 'return', None),
        ('Backend API', 'FuelRecord Model', '7: create new FuelRecord', 8.0, 'sync', None),
        ('FuelRecord Model', 'FuelRecord Model', '8: calculate fuel metrics', 7.7, 'self', None),
        ('FuelRecord Model', 'Database', '9: save fuel record', 7.4, 'async', None),
        ('Database', 'FuelRecord Model', '10: return saved record', 7.1, 'return', None),
        ('Backend API', 'ML Service', '11: requestMLPrediction(vehicleId)', 6.8, 'async', None),
        ('ML Service', 'ML Service', '12: load ML model', 6.5, 'self', None),
        ('ML Service', 'ML Service', '13: generate prediction', 6.2, 'self', None),
        ('ML Service', 'Database', '14: save ML prediction', 5.9, 'async', None),
        ('ML Service', 'Backend API', '15: return prediction results', 5.6, 'return', None),
        ('Backend API', 'AI Service', '16: generateRecommendation(vehicleData)', 5.3, 'async', None),
        ('AI Service', 'AI Service', '17: analyze fuel patterns', 5.0, 'self', None),
        ('AI Service', 'AI Service', '18: call Gemini AI API', 4.7, 'self', None),
        ('AI Service', 'Recommendation', '19: create AI recommendation', 4.4, 'sync', None),
        ('Recommendation', 'Database', '20: save recommendation', 4.1, 'async', None),
        ('AI Service', 'Backend API', '21: return recommendation', 3.8, 'return', None),
        ('Backend API', 'ApiService', '22: return complete response', 3.5, 'return', None),
        ('ApiService', 'FuelRecordsPage', '23: update UI with new record', 3.2, 'return', None),
        ('FuelRecordsPage', 'User', '24: show success & recommendations', 2.9, 'async', None),
    ]
    
    draw_sequence_messages(ax, actors, sequences)
    
    # Add activation boxes for active periods
    activation_periods = [
        ('Backend API', 8.9, 3.5),
        ('ML Service', 6.8, 5.6),
        ('AI Service', 5.3, 3.8),
    ]
    
    for actor, start_y, end_y in activation_periods:
        x_pos = actors[actor]
        rect = Rectangle((x_pos-0.05, end_y), 0.1, start_y-end_y, 
                        facecolor='yellow', alpha=0.3)
        ax.add_patch(rect)
    
    plt.tight_layout()
    return fig

def create_vehicle_negotiation_sequence():
    """Generate sequence diagram for AI-powered vehicle negotiation"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 14))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # Title
    ax.text(8, 13.5, 'AutoGuardian - Vehicle Negotiation Sequence', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    ax.text(8, 13.2, 'AI-Powered Vehicle Sales Negotiation Flow', 
            ha='center', va='center', fontsize=12, style='italic')
    
    # Define actors
    actors = {
        'Buyer': 2,
        'MarketplacePage': 4,
        'ApiService': 6,
        'Backend API': 8,
        'NegotiationBot': 10,
        'GenAI Service': 12,
        'Database': 14
    }
    
    # Draw actor boxes and lifelines
    y_top = 12.5
    y_bottom = 1
    
    for actor, x_pos in actors.items():
        color = '#8B5CF6' if 'AI' in actor or 'Bot' in actor else '#EF4444'
        box = FancyBboxPatch((x_pos-0.6, y_top-0.2), 1.2, 0.4,
                            boxstyle="round,pad=0.02", 
                            facecolor=color, alpha=0.8, 
                            edgecolor='black', linewidth=1)
        ax.add_patch(box)
        ax.text(x_pos, y_top, actor, ha='center', va='center', 
                fontsize=8, color='white', fontweight='bold')
        
        # Lifeline
        ax.plot([x_pos, x_pos], [y_top-0.2, y_bottom], 
                linestyle='--', color='gray', alpha=0.7, linewidth=1)
    
    # Define negotiation sequence
    sequences = [
        ('Buyer', 'MarketplacePage', '1: Browse vehicle listings', 11.8, 'sync', None),
        ('Buyer', 'MarketplacePage', '2: Select vehicle & start negotiation', 11.5, 'sync', None),
        ('MarketplacePage', 'ApiService', '3: startNegotiation(vehicleId, buyerInfo)', 11.2, 'async', None),
        ('ApiService', 'Backend API', '4: POST /api/negotiations/start', 10.9, 'async', None),
        ('Backend API', 'Database', '5: create negotiation record', 10.6, 'async', None),
        ('Backend API', 'NegotiationBot', '6: initializeNegotiation(vehicleData)', 10.3, 'sync', None),
        ('NegotiationBot', 'Backend API', '7: return initial bot message', 10.0, 'return', None),
        ('Backend API', 'ApiService', '8: return negotiation started', 9.7, 'return', None),
        ('ApiService', 'MarketplacePage', '9: show negotiation chat', 9.4, 'return', None),
        ('MarketplacePage', 'Buyer', '10: display bot welcome message', 9.1, 'async', None),
        
        # Negotiation rounds
        ('Buyer', 'MarketplacePage', '11: "I offer $15,000"', 8.6, 'sync', None),
        ('MarketplacePage', 'ApiService', '12: sendNegotiationMessage(message)', 8.3, 'async', None),
        ('ApiService', 'Backend API', '13: POST /api/negotiations/continue', 8.0, 'async', None),
        ('Backend API', 'NegotiationBot', '14: processMessage("I offer $15,000")', 7.7, 'sync', None),
        ('NegotiationBot', 'NegotiationBot', '15: extractPrice($15,000)', 7.4, 'self', None),
        ('NegotiationBot', 'NegotiationBot', '16: analyzeIntent(OFFER)', 7.1, 'self', None),
        ('NegotiationBot', 'GenAI Service', '17: generateResponse(context)', 6.8, 'async', None),
        ('GenAI Service', 'GenAI Service', '18: call Gemini AI API', 6.5, 'self', None),
        ('GenAI Service', 'NegotiationBot', '19: return AI response', 6.2, 'return', None),
        ('NegotiationBot', 'NegotiationBot', '20: calculateCounterOffer($16,500)', 5.9, 'self', None),
        ('NegotiationBot', 'Database', '21: update chat history', 5.6, 'async', None),
        ('NegotiationBot', 'Backend API', '22: return bot response', 5.3, 'return', None),
        ('Backend API', 'ApiService', '23: return negotiation response', 5.0, 'return', None),
        ('ApiService', 'MarketplacePage', '24: update chat with bot message', 4.7, 'return', None),
        ('MarketplacePage', 'Buyer', '25: "How about $16,500? This car has..."', 4.4, 'async', None),
        
        # Final acceptance
        ('Buyer', 'MarketplacePage', '26: "I accept $16,500"', 3.9, 'sync', None),
        ('MarketplacePage', 'ApiService', '27: acceptOffer(negotiationId)', 3.6, 'async', None),
        ('ApiService', 'Backend API', '28: POST /api/negotiations/accept', 3.3, 'async', None),
        ('Backend API', 'Database', '29: mark negotiation as accepted', 3.0, 'async', None),
        ('Backend API', 'Database', '30: update vehicle status to sold', 2.7, 'async', None),
        ('Backend API', 'ApiService', '31: return acceptance confirmation', 2.4, 'return', None),
        ('ApiService', 'MarketplacePage', '32: show success message', 2.1, 'return', None),
        ('MarketplacePage', 'Buyer', '33: "Deal accepted! Contact details..."', 1.8, 'async', None),
    ]
    
    draw_sequence_messages(ax, actors, sequences)
    
    # Add AI processing highlight
    ai_box = Rectangle((9.5, 5.0), 3, 2.2, facecolor='#8B5CF6', alpha=0.1, 
                      edgecolor='#8B5CF6', linewidth=2, linestyle='dashed')
    ax.add_patch(ai_box)
    ax.text(11, 6.8, 'AI Processing', ha='center', va='center', 
            fontsize=9, fontweight='bold', color='#8B5CF6')
    
    plt.tight_layout()
    return fig

def create_ml_prediction_sequence():
    """Generate sequence diagram for ML prediction generation"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(8, 9.5, 'AutoGuardian - ML Prediction Generation Sequence', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    ax.text(8, 9.2, 'Machine Learning Fuel Consumption Prediction Flow', 
            ha='center', va='center', fontsize=12, style='italic')
    
    # Define actors
    actors = {
        'User': 1.5,
        'AIInsightsPage': 3.5,
        'ApiService': 5.5,
        'Backend API': 7.5,
        'ML Service': 9.5,
        'FeatureProcessor': 11.5,
        'Database': 13.5,
        'Vehicle Model': 15
    }
    
    # Draw actor boxes and lifelines
    y_top = 8.5
    y_bottom = 1
    
    for actor, x_pos in actors.items():
        color = '#7C3AED' if 'ML' in actor or 'Feature' in actor else '#059669'
        box = FancyBboxPatch((x_pos-0.6, y_top-0.2), 1.2, 0.4,
                            boxstyle="round,pad=0.02", 
                            facecolor=color, alpha=0.8, 
                            edgecolor='black', linewidth=1)
        ax.add_patch(box)
        ax.text(x_pos, y_top, actor, ha='center', va='center', 
                fontsize=8, color='white', fontweight='bold')
        
        # Lifeline
        ax.plot([x_pos, x_pos], [y_top-0.2, y_bottom], 
                linestyle='--', color='gray', alpha=0.7, linewidth=1)
    
    # Define ML prediction sequence
    sequences = [
        ('User', 'AIInsightsPage', '1: Select vehicle for prediction', 7.8, 'sync', None),
        ('User', 'AIInsightsPage', '2: Click "Generate ML Prediction"', 7.5, 'sync', None),
        ('AIInsightsPage', 'ApiService', '3: generateMLPrediction(vehicleId)', 7.2, 'async', None),
        ('ApiService', 'Backend API', '4: POST /api/predictions/generate', 6.9, 'async', None),
        ('Backend API', 'Vehicle Model', '5: getVehicleFeatures(vehicleId)', 6.6, 'sync', None),
        ('Vehicle Model', 'Database', '6: query vehicle data', 6.3, 'sync', None),
        ('Database', 'Vehicle Model', '7: return vehicle details', 6.0, 'return', None),
        ('Vehicle Model', 'Backend API', '8: return vehicle features', 5.7, 'return', None),
        ('Backend API', 'FeatureProcessor', '9: processFeatures(vehicleData)', 5.4, 'sync', None),
        ('FeatureProcessor', 'FeatureProcessor', '10: standardize make/model', 5.1, 'self', None),
        ('FeatureProcessor', 'FeatureProcessor', '11: normalize numeric values', 4.8, 'self', None),
        ('FeatureProcessor', 'Backend API', '12: return processed features', 4.5, 'return', None),
        ('Backend API', 'ML Service', '13: predict(processedFeatures)', 4.2, 'sync', None),
        ('ML Service', 'ML Service', '14: load trained model', 3.9, 'self', None),
        ('ML Service', 'ML Service', '15: run prediction algorithm', 3.6, 'self', None),
        ('ML Service', 'ML Service', '16: calculate confidence score', 3.3, 'self', None),
        ('ML Service', 'Backend API', '17: return prediction results', 3.0, 'return', None),
        ('Backend API', 'Database', '18: save ML prediction', 2.7, 'async', None),
        ('Backend API', 'ApiService', '19: return prediction response', 2.4, 'return', None),
        ('ApiService', 'AIInsightsPage', '20: update UI with predictions', 2.1, 'return', None),
        ('AIInsightsPage', 'User', '21: display prediction results', 1.8, 'async', None),
    ]
    
    draw_sequence_messages(ax, actors, sequences)
    
    # Add ML processing highlight
    ml_box = Rectangle((8.5, 3.0), 4, 1.5, facecolor='#7C3AED', alpha=0.1, 
                      edgecolor='#7C3AED', linewidth=2, linestyle='dashed')
    ax.add_patch(ml_box)
    ax.text(10.5, 3.8, 'ML Processing', ha='center', va='center', 
            fontsize=9, fontweight='bold', color='#7C3AED')
    
    plt.tight_layout()
    return fig

def draw_sequence_messages(ax, actors, sequences):
    """Draw sequence messages between actors"""
    
    for seq in sequences:
        from_actor, to_actor, message, y_pos, msg_type, return_msg = seq
        
        from_x = actors[from_actor]
        to_x = actors[to_actor]
        
        if msg_type == 'self':
            # Self-call (loop back)
            ax.add_patch(Rectangle((from_x, y_pos-0.05), 0.8, 0.1, 
                                 facecolor='yellow', alpha=0.3))
            ax.annotate('', xy=(from_x+0.8, y_pos), xytext=(from_x, y_pos),
                       arrowprops=dict(arrowstyle='->', color='blue', lw=1.2))
            ax.text(from_x+0.4, y_pos+0.15, message, ha='center', va='bottom', 
                   fontsize=7, color='blue')
        else:
            # Regular message between actors
            if msg_type == 'return':
                # Return message (dashed line)
                ax.annotate('', xy=(from_x, y_pos), xytext=(to_x, y_pos),
                           arrowprops=dict(arrowstyle='->', color='green', 
                                         lw=1, linestyle='dashed'))
                color = 'green'
            elif msg_type == 'async':
                # Async message (solid line with open arrow)
                ax.annotate('', xy=(to_x, y_pos), xytext=(from_x, y_pos),
                           arrowprops=dict(arrowstyle='->', color='red', lw=1.2))
                color = 'red'
            else:
                # Sync message (solid line)
                ax.annotate('', xy=(to_x, y_pos), xytext=(from_x, y_pos),
                           arrowprops=dict(arrowstyle='->', color='black', lw=1.2))
                color = 'black'
            
            # Message label
            mid_x = (from_x + to_x) / 2
            ax.text(mid_x, y_pos+0.1, message, ha='center', va='bottom', 
                   fontsize=7, color=color, 
                   bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.8))

def create_dashboard_analytics_sequence():
    """Generate sequence diagram for dashboard analytics loading"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'AutoGuardian - Dashboard Analytics Sequence', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    ax.text(7, 9.2, 'Real-time Analytics and Data Visualization Loading', 
            ha='center', va='center', fontsize=12, style='italic')
    
    # Define actors
    actors = {
        'User': 1.5,
        'Dashboard': 3.5,
        'ApiService': 5.5,
        'Analytics API': 7.5,
        'Database': 9.5,
        'Charts Library': 11.5,
        'Cache': 13
    }
    
    # Draw actor boxes and lifelines
    y_top = 8.5
    y_bottom = 1.5
    
    for actor, x_pos in actors.items():
        box = FancyBboxPatch((x_pos-0.6, y_top-0.2), 1.2, 0.4,
                            boxstyle="round,pad=0.02", 
                            facecolor='#F59E0B', alpha=0.8, 
                            edgecolor='black', linewidth=1)
        ax.add_patch(box)
        ax.text(x_pos, y_top, actor, ha='center', va='center', 
                fontsize=8, color='white', fontweight='bold')
        
        # Lifeline
        ax.plot([x_pos, x_pos], [y_top-0.2, y_bottom], 
                linestyle='--', color='gray', alpha=0.7, linewidth=1)
    
    # Define analytics loading sequence
    sequences = [
        ('User', 'Dashboard', '1: Navigate to Dashboard', 7.8, 'sync', None),
        ('Dashboard', 'Dashboard', '2: useEffect() triggered', 7.5, 'self', None),
        ('Dashboard', 'ApiService', '3: getDashboardAnalytics()', 7.2, 'async', None),
        ('ApiService', 'Cache', '4: checkCachedData()', 6.9, 'sync', None),
        ('Cache', 'ApiService', '5: return null (cache miss)', 6.6, 'return', None),
        ('ApiService', 'Analytics API', '6: GET /api/analytics/dashboard', 6.3, 'async', None),
        ('Analytics API', 'Database', '7: query fuel records', 6.0, 'sync', None),
        ('Analytics API', 'Database', '8: query vehicle data', 5.7, 'sync', None),
        ('Analytics API', 'Database', '9: query recommendations', 5.4, 'sync', None),
        ('Database', 'Analytics API', '10: return aggregated data', 5.1, 'return', None),
        ('Analytics API', 'Analytics API', '11: calculate statistics', 4.8, 'self', None),
        ('Analytics API', 'Analytics API', '12: format response data', 4.5, 'self', None),
        ('Analytics API', 'Cache', '13: cacheResults(data)', 4.2, 'async', None),
        ('Analytics API', 'ApiService', '14: return analytics data', 3.9, 'return', None),
        ('ApiService', 'Dashboard', '15: return formatted data', 3.6, 'return', None),
        ('Dashboard', 'Charts Library', '16: renderCharts(data)', 3.3, 'async', None),
        ('Charts Library', 'Dashboard', '17: return chart components', 3.0, 'return', None),
        ('Dashboard', 'User', '18: display analytics dashboard', 2.7, 'async', None),
    ]
    
    draw_sequence_messages(ax, actors, sequences)
    
    plt.tight_layout()
    return fig

def main():
    """Generate all sequence diagrams"""
    print("Generating AutoGuardian Sequence Diagrams...")
    
    diagrams = [
        ("User Login Flow", create_user_login_sequence, "AutoGuardian_Login_Sequence.png"),
        ("Add Fuel Record Flow", create_fuel_record_sequence, "AutoGuardian_FuelRecord_Sequence.png"),
        ("Vehicle Negotiation Flow", create_vehicle_negotiation_sequence, "AutoGuardian_Negotiation_Sequence.png"),
        ("ML Prediction Flow", create_ml_prediction_sequence, "AutoGuardian_MLPrediction_Sequence.png"),
        ("Dashboard Analytics Flow", create_dashboard_analytics_sequence, "AutoGuardian_Analytics_Sequence.png"),
    ]
    
    base_path = r"C:\Users\chan-shinan\Documents\icbt\final project\shinan_final_project\autoguardian-fuel-system"
    
    for diagram_name, create_func, filename in diagrams:
        print(f"Creating {diagram_name}...")
        fig = create_func()
        output_path = f"{base_path}\\{filename}"
        fig.savefig(output_path, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        print(f"Saved: {output_path}")
        plt.close(fig)
    
    print("\n[SUCCESS] All sequence diagrams generated!")
    print("\nGenerated Diagrams:")
    print("1. User Login Sequence - Authentication flow")
    print("2. Add Fuel Record Sequence - Complete fuel tracking with ML & AI")
    print("3. Vehicle Negotiation Sequence - AI-powered sales negotiation")
    print("4. ML Prediction Sequence - Machine learning prediction generation")
    print("5. Dashboard Analytics Sequence - Real-time dashboard data loading")
    
    print("\nFeatures:")
    print("- UML sequence diagram notation")
    print("- Actor lifelines and activation boxes")
    print("- Sync/Async/Return message types")
    print("- Self-calls and loops")
    print("- Color-coded message flows")
    print("- Detailed interaction flows")

if __name__ == "__main__":
    main()