#!/usr/bin/env python3
"""
AutoGuardian Fuel Management System - Clear Class Diagram Generator
This script generates high-quality, readable UML class diagrams with proper text sizing and formatting.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_clear_class_diagram():
    """Generate clear, readable UML class diagram with optimized text sizing"""
    
    # Create large figure for better readability
    fig, ax = plt.subplots(1, 1, figsize=(20, 14))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # Define colors
    colors = {
        'model': '#2563EB',        # Blue - Database Models
        'service': '#059669',      # Green - Service Classes  
        'ai': '#7C3AED',          # Purple - AI/ML Classes
        'frontend': '#DC2626',     # Red - Frontend Components
        'config': '#4B5563',      # Gray - Configuration
        'background': '#F9FAFB'   # Light background
    }
    
    # Set background
    ax.add_patch(patches.Rectangle((0, 0), 20, 14, facecolor=colors['background'], alpha=0.3))
    
    # Main title
    ax.text(10, 13.5, 'AutoGuardian Fuel Management System', 
            ha='center', va='center', fontsize=20, fontweight='bold', color='black')
    ax.text(10, 13, 'UML Class Diagram - Core Components', 
            ha='center', va='center', fontsize=14, style='italic', color='#374151')
    
    # Define core classes with essential information only
    classes = {
        'User': {
            'pos': (3, 10.5),
            'size': (3.2, 2.5),
            'color': colors['model'],
            'attributes': [
                '+id: Integer',
                '+username: String(50)',
                '+email: String(100)', 
                '+first_name: String(50)',
                '+phone: String(20)',
                '+is_active: Boolean',
                '-password_hash: String'
            ],
            'methods': [
                '+set_password(password)',
                '+check_password(): Boolean',
                '+generate_tokens(): Dict',
                '+to_dict(): Dict'
            ]
        },
        
        'Vehicle': {
            'pos': (7.5, 10.5),
            'size': (3.5, 3),
            'color': colors['model'],
            'attributes': [
                '+id: Integer',
                '+user_id: Integer (FK)',
                '+vehicle_name: String(100)',
                '+make: String(50)',
                '+model: String(50)',
                '+year: Integer',
                '+engine_size: Numeric',
                '+fuel_type: String(20)',
                '+tank_capacity: Numeric',
                '+is_active: Boolean'
            ],
            'methods': [
                '+display_name: String',
                '+current_odometer: Integer',
                '+calculate_average_consumption()',
                '+to_dict(): Dict'
            ]
        },
        
        'FuelRecord': {
            'pos': (12.5, 10.5),
            'size': (3.8, 3),
            'color': colors['model'],
            'attributes': [
                '+id: Integer',
                '+vehicle_id: Integer (FK)',
                '+record_date: Date',
                '+existing_tank_percentage: Numeric',
                '+after_refuel_percentage: Numeric',
                '+odometer_value: Integer',
                '+driving_type: Enum',
                '+fuel_price: Numeric',
                '+total_cost: Numeric'
            ],
            'methods': [
                '+calculate_fuel_metrics()',
                '+validate_odometer(): Boolean',
                '+to_dict(): Dict'
            ]
        },
        
        'AIRecommendation': {
            'pos': (17, 10.5),
            'size': (2.8, 2.5),
            'color': colors['ai'],
            'attributes': [
                '+id: Integer',
                '+user_id: Integer (FK)',
                '+vehicle_id: Integer (FK)',
                '+title: String(200)',
                '+recommendation_text: Text',
                '+priority_level: String',
                '+is_read: Boolean'
            ],
            'methods': [
                '+mark_as_read()',
                '+calculate_savings(): Dict',
                '+to_dict(): Dict'
            ]
        },
        
        'FuelConsumptionPredictor': {
            'pos': (3, 6.5),
            'size': (3.5, 2.2),
            'color': colors['ai'],
            'attributes': [
                '-model_path: String',
                '-model: ML_Model',
                '-is_loaded: Boolean'
            ],
            'methods': [
                '+load_model(): Boolean',
                '+preprocess_features(): Dict',
                '+predict(vehicle_data): Dict',
                '+validate_input(): Boolean'
            ]
        },
        
        'GenAIRecommendationService': {
            'pos': (7.5, 6.5),
            'size': (4, 2.2),
            'color': colors['ai'],
            'attributes': [
                '-api_key: String',
                '-model: GenAI_Model',
                '-is_configured: Boolean'
            ],
            'methods': [
                '+configure_genai()',
                '+generate_maintenance_rec(): Dict',
                '+generate_efficiency_rec(): Dict',
                '+test_connection(): Dict'
            ]
        },
        
        'NegotiationBot': {
            'pos': (12.5, 6.5),
            'size': (3.5, 2.2),
            'color': colors['service'],
            'attributes': [
                '-genai_service: GenAIService',
                '-use_ai: Boolean'
            ],
            'methods': [
                '+extract_price(message): Float',
                '+generate_response(): String',
                '+analyze_intent(): Dict',
                '+calculate_counter_offer(): Float'
            ]
        },
        
        'AuthService': {
            'pos': (3, 3),
            'size': (3, 1.8),
            'color': colors['frontend'],
            'attributes': [
                '+baseURL: String'
            ],
            'methods': [
                '+login(credentials): Promise',
                '+register(userData): Promise',
                '+logout(): void',
                '+isAuthenticated(): Boolean'
            ]
        },
        
        'ApiService': {
            'pos': (7.5, 3),
            'size': (4, 2.2),
            'color': colors['frontend'],
            'attributes': [
                '+baseURL: String',
                '+authToken: String'
            ],
            'methods': [
                '+getVehicles(): Promise',
                '+addFuelRecord(): Promise',
                '+generateMLPrediction(): Promise',
                '+getDashboardAnalytics(): Promise',
                '+createVehicleSale(): Promise'
            ]
        },
        
        'Dashboard': {
            'pos': (13, 3),
            'size': (3, 1.8),
            'color': colors['frontend'],
            'attributes': [
                '+analytics: Object',
                '+isLoading: Boolean'
            ],
            'methods': [
                '+fetchAnalytics(): Promise',
                '+renderCharts(): JSX',
                '+render(): JSX'
            ]
        },
        
        'VehiclesPage': {
            'pos': (17, 3),
            'size': (2.5, 1.8),
            'color': colors['frontend'],
            'attributes': [
                '+vehicles: Array',
                '+showModal: Boolean'
            ],
            'methods': [
                '+fetchVehicles(): Promise',
                '+handleSubmit(): Promise',
                '+render(): JSX'
            ]
        }
    }
    
    # Draw all classes with improved text formatting
    for class_name, details in classes.items():
        draw_clear_class_box(ax, class_name, details)
    
    # Define key relationships
    relationships = [
        # Core model relationships
        ('User', 'Vehicle', 'composition', '1', '*', 'owns'),
        ('User', 'AIRecommendation', 'association', '1', '*', 'receives'),
        ('Vehicle', 'FuelRecord', 'composition', '1', '*', 'tracks'),
        
        # Service dependencies
        ('GenAIRecommendationService', 'AIRecommendation', 'dependency', '', '', 'creates'),
        ('FuelConsumptionPredictor', 'Vehicle', 'dependency', '', '', 'analyzes'),
        ('NegotiationBot', 'GenAIRecommendationService', 'dependency', '', '', 'uses'),
        
        # Frontend to backend
        ('AuthService', 'User', 'dependency', '', '', 'authenticates'),
        ('ApiService', 'Vehicle', 'dependency', '', '', 'manages'),
        ('Dashboard', 'ApiService', 'dependency', '', '', 'uses'),
        ('VehiclesPage', 'ApiService', 'dependency', '', '', 'uses'),
    ]
    
    # Draw relationships
    for source, target, rel_type, mult1, mult2, label in relationships:
        if source in classes and target in classes:
            draw_clear_relationship(ax, classes[source], classes[target], rel_type, mult1, mult2, label)
    
    # Add layer labels with better positioning
    ax.text(1, 11.5, 'DATABASE\nMODELS', ha='center', va='center', 
            fontsize=11, fontweight='bold', rotation=90,
            bbox=dict(boxstyle="round,pad=0.3", facecolor=colors['model'], alpha=0.8, edgecolor='white'))
    
    ax.text(1, 7.5, 'AI/ML\nSERVICES', ha='center', va='center', 
            fontsize=11, fontweight='bold', rotation=90,
            bbox=dict(boxstyle="round,pad=0.3", facecolor=colors['ai'], alpha=0.8, edgecolor='white'))
    
    ax.text(1, 3.5, 'FRONTEND\nCOMPONENTS', ha='center', va='center', 
            fontsize=11, fontweight='bold', rotation=90,
            bbox=dict(boxstyle="round,pad=0.3", facecolor=colors['frontend'], alpha=0.8, edgecolor='white'))
    
    # Enhanced legend
    legend_elements = [
        patches.Rectangle((0, 0), 1, 1, facecolor=colors['model'], alpha=0.8, label='Database Models'),
        patches.Rectangle((0, 0), 1, 1, facecolor=colors['ai'], alpha=0.8, label='AI/ML Services'),
        patches.Rectangle((0, 0), 1, 1, facecolor=colors['service'], alpha=0.8, label='Service Classes'),
        patches.Rectangle((0, 0), 1, 1, facecolor=colors['frontend'], alpha=0.8, label='Frontend Components'),
    ]
    
    ax.legend(handles=legend_elements, loc='lower right', bbox_to_anchor=(0.98, 0.02), 
             fontsize=10, framealpha=0.9)
    
    # Add UML notation guide
    ax.text(0.5, 1.5, 'UML Notation Guide:', fontsize=11, fontweight='bold', color='#374151')
    ax.text(0.5, 1.2, '+ Public attribute/method', fontsize=9, color='#374151')
    ax.text(0.5, 1.0, '- Private attribute/method', fontsize=9, color='#374151')
    ax.text(0.5, 0.8, '♦——→ Composition (owns)', fontsize=9, color='#374151')
    ax.text(0.5, 0.6, '——→ Association (uses)', fontsize=9, color='#374151')
    ax.text(0.5, 0.4, '- - → Dependency', fontsize=9, color='#374151')
    ax.text(0.5, 0.2, '1, * Multiplicity', fontsize=9, color='#374151')
    
    plt.tight_layout()
    return fig

def draw_clear_class_box(ax, class_name, details):
    """Draw a clear, readable UML class box"""
    x, y = details['pos']
    width, height = details['size']
    color = details['color']
    
    # Main class box with better styling
    box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                        boxstyle="round,pad=0.03", 
                        facecolor=color, alpha=0.9, 
                        edgecolor='#1F2937', linewidth=1.5)
    ax.add_patch(box)
    
    # Calculate text positioning with better spacing
    text_y_start = y + height/2 - 0.15
    line_height = 0.13
    
    # Class name - larger and more prominent
    ax.text(x, text_y_start, class_name, ha='center', va='center', 
            fontsize=11, fontweight='bold', color='white')
    
    # Separator line after class name
    separator_y = text_y_start - 0.08
    ax.plot([x - width/2 + 0.1, x + width/2 - 0.1], 
            [separator_y, separator_y], 
            color='white', linewidth=1.2, alpha=0.8)
    
    # Attributes section with better font size
    current_y = separator_y - 0.15
    max_attrs = min(len(details['attributes']), int((height - 1) / line_height))
    
    for i, attr in enumerate(details['attributes'][:max_attrs]):
        if current_y > y - height/2 + 0.15:
            ax.text(x - width/2 + 0.08, current_y, attr, 
                   ha='left', va='center', fontsize=8.5, color='white', 
                   fontfamily='monospace')
            current_y -= line_height
    
    # Separator line before methods
    if details['methods'] and current_y > y - height/2 + 0.15:
        method_separator_y = current_y + 0.05
        ax.plot([x - width/2 + 0.1, x + width/2 - 0.1], 
                [method_separator_y, method_separator_y], 
                color='white', linewidth=1.2, alpha=0.8)
        current_y = method_separator_y - 0.1
    
    # Methods section
    max_methods = min(len(details['methods']), int((current_y - (y - height/2 + 0.15)) / line_height))
    
    for i, method in enumerate(details['methods'][:max_methods]):
        if current_y > y - height/2 + 0.15:
            ax.text(x - width/2 + 0.08, current_y, method, 
                   ha='left', va='center', fontsize=8.5, color='white',
                   fontfamily='monospace')
            current_y -= line_height

def draw_clear_relationship(ax, source_class, target_class, rel_type, mult1, mult2, label):
    """Draw clear relationship lines with better visibility"""
    x1, y1 = source_class['pos']
    x2, y2 = target_class['pos']
    w1, h1 = source_class['size']
    w2, h2 = target_class['size']
    
    # Calculate connection points
    if abs(x2 - x1) > abs(y2 - y1):
        if x2 > x1:
            conn_x1, conn_y1 = x1 + w1/2, y1
            conn_x2, conn_y2 = x2 - w2/2, y2
        else:
            conn_x1, conn_y1 = x1 - w1/2, y1
            conn_x2, conn_y2 = x2 + w2/2, y2
    else:
        if y2 > y1:
            conn_x1, conn_y1 = x1, y1 + h1/2
            conn_x2, conn_y2 = x2, y2 - h2/2
        else:
            conn_x1, conn_y1 = x1, y1 - h1/2
            conn_x2, conn_y2 = x2, y2 + h2/2
    
    # Draw relationship based on type
    if rel_type == 'composition':
        # Composition with filled diamond
        ax.annotate('', xy=(conn_x2, conn_y2), xytext=(conn_x1, conn_y1),
                   arrowprops=dict(arrowstyle='->', color='#1F2937', lw=1.8))
        # Add filled diamond
        diamond = patches.RegularPolygon((conn_x1, conn_y1), 4, radius=0.08, 
                                       orientation=np.pi/4, facecolor='#1F2937', 
                                       edgecolor='#1F2937')
        ax.add_patch(diamond)
        
    elif rel_type == 'association':
        # Simple association
        ax.annotate('', xy=(conn_x2, conn_y2), xytext=(conn_x1, conn_y1),
                   arrowprops=dict(arrowstyle='->', color='#374151', lw=1.5))
        
    elif rel_type == 'dependency':
        # Dashed dependency
        ax.annotate('', xy=(conn_x2, conn_y2), xytext=(conn_x1, conn_y1),
                   arrowprops=dict(arrowstyle='->', color='#6B7280', lw=1.2, linestyle='dashed'))
    
    # Add multiplicity labels
    if mult1:
        ax.text(conn_x1, conn_y1 + 0.18, mult1, ha='center', va='center', 
               fontsize=9, fontweight='bold', color='#1F2937',
               bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.8))
    if mult2:
        ax.text(conn_x2, conn_y2 + 0.18, mult2, ha='center', va='center', 
               fontsize=9, fontweight='bold', color='#1F2937',
               bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.8))
    
    # Add relationship label
    if label:
        mid_x = (conn_x1 + conn_x2) / 2
        mid_y = (conn_y1 + conn_y2) / 2
        ax.text(mid_x, mid_y - 0.15, label, ha='center', va='center', 
               fontsize=8, style='italic', color='#374151',
               bbox=dict(boxstyle="round,pad=0.15", facecolor='white', alpha=0.9,
                        edgecolor='#D1D5DB', linewidth=0.5))

def create_backend_focus_diagram():
    """Create a focused diagram showing backend database models in detail"""
    
    fig, ax = plt.subplots(1, 1, figsize=(18, 12))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Set background
    ax.add_patch(patches.Rectangle((0, 0), 18, 12, facecolor='#F9FAFB', alpha=0.5))
    
    # Title
    ax.text(9, 11.5, 'AutoGuardian Backend - Database Models', 
            ha='center', va='center', fontsize=18, fontweight='bold', color='#1F2937')
    ax.text(9, 11.1, 'Detailed Class Diagram with Relationships', 
            ha='center', va='center', fontsize=12, style='italic', color='#6B7280')
    
    # Define backend models with full detail
    backend_models = {
        'User': {
            'pos': (3, 8.5),
            'size': (3.5, 3.2),
            'color': '#1E40AF',
            'attributes': [
                '+id: Integer (PK)',
                '+username: String(50) ✓',
                '+email: String(100) ✓',
                '+first_name: String(50)',
                '+last_name: String(50)',
                '+phone: String(20)',
                '+is_active: Boolean',
                '+created_at: DateTime',
                '+updated_at: DateTime',
                '-password_hash: String(255)'
            ],
            'methods': [
                '+set_password(password): void',
                '+check_password(pwd): Boolean',
                '+generate_tokens(): Dict',
                '+to_dict(): Dict',
                '@property +full_name: String',
                '@classmethod +find_by_email(): User'
            ]
        },
        
        'Vehicle': {
            'pos': (8.5, 8.5),
            'size': (4, 3.5),
            'color': '#1E40AF',
            'attributes': [
                '+id: Integer (PK)',
                '+user_id: Integer (FK)',
                '+vehicle_name: String(100)',
                '+make: String(50)',
                '+model: String(50)',
                '+year: Integer',
                '+engine_size: Numeric(3,1)',
                '+fuel_type: String(20)',
                '+tank_capacity: Numeric(5,2)',
                '+is_active: Boolean',
                '+created_at: DateTime'
            ],
            'methods': [
                '@property +display_name: String',
                '@property +current_odometer: Integer',
                '+get_ml_features(): Dict',
                '+calculate_avg_consumption(): Float',
                '+to_dict(): Dict'
            ]
        },
        
        'FuelRecord': {
            'pos': (14, 8.5),
            'size': (3.5, 3.8),
            'color': '#1E40AF',
            'attributes': [
                '+id: Integer (PK)',
                '+vehicle_id: Integer (FK)',
                '+record_date: Date',
                '+record_time: Time',
                '+existing_tank_%: Numeric',
                '+after_refuel_%: Numeric',
                '+odometer_value: Integer',
                '+driving_type: Enum',
                '+location: String(100)',
                '+fuel_price: Numeric(6,2)',
                '+total_cost: Numeric(8,2)',
                '+notes: Text'
            ],
            'methods': [
                '-_calculate_fuel_metrics(): void',
                '+validate_odometer(): Boolean',
                '@property +efficiency_rating: String',
                '+to_dict(): Dict'
            ]
        },
        
        'AIRecommendation': {
            'pos': (3, 4),
            'size': (4, 3),
            'color': '#7C2D12',
            'attributes': [
                '+id: Integer (PK)',
                '+user_id: Integer (FK)',
                '+vehicle_id: Integer (FK)',
                '+recommendation_type: String(20)',
                '+title: String(200)',
                '+recommendation_text: Text',
                '+priority_level: String(20)',
                '+impact_score: Numeric(3,2)',
                '+is_read: Boolean',
                '+created_at: DateTime',
                '+expires_at: DateTime'
            ],
            'methods': [
                '@property +is_expired: Boolean',
                '+mark_as_read(): void',
                '+calculate_savings(): Dict',
                '+to_dict(): Dict',
                '@classmethod +get_user_recs(): List'
            ]
        },
        
        'VehicleSale': {
            'pos': (9, 4),
            'size': (3.5, 2.5),
            'color': '#166534',
            'attributes': [
                '+id: Integer (PK)',
                '+user_id: Integer (FK)',
                '+vehicle_id: Integer (FK)',
                '+selling_price: Float',
                '+features: JSON',
                '+description: Text',
                '+is_active: Boolean',
                '+is_sold: Boolean',
                '-minimum_price: Float'
            ],
            'methods': [
                '+to_dict(): Dict',
                '+update_sale(): void',
                '+mark_as_sold(): void'
            ]
        },
        
        'Negotiation': {
            'pos': (14, 4),
            'size': (3.5, 2.5),
            'color': '#166534',
            'attributes': [
                '+id: Integer (PK)',
                '+vehicle_sale_id: Integer (FK)',
                '+buyer_name: String(100)',
                '+buyer_email: String(150)',
                '+final_offer: Float',
                '+chat_history: JSON',
                '+status: String(20)',
                '+created_at: DateTime'
            ],
            'methods': [
                '+update_status(status): void',
                '+add_chat_message(): void',
                '+to_dict(): Dict'
            ]
        }
    }
    
    # Draw all backend models
    for model_name, details in backend_models.items():
        draw_detailed_model_box(ax, model_name, details)
    
    # Define relationships with detailed notation
    relationships = [
        ('User', 'Vehicle', 'composition', '1', '0..*', 'owns'),
        ('User', 'AIRecommendation', 'association', '1', '0..*', 'receives'),
        ('User', 'VehicleSale', 'composition', '1', '0..*', 'creates'),
        ('Vehicle', 'FuelRecord', 'composition', '1', '0..*', 'has'),
        ('Vehicle', 'AIRecommendation', 'association', '1', '0..*', 'generates'),
        ('VehicleSale', 'Negotiation', 'composition', '1', '0..*', 'negotiated'),
    ]
    
    # Draw relationships
    for source, target, rel_type, mult1, mult2, label in relationships:
        if source in backend_models and target in backend_models:
            draw_detailed_relationship(ax, backend_models[source], backend_models[target], 
                                     rel_type, mult1, mult2, label)
    
    # Add constraint information
    constraints = [
        "Database Constraints & Notes:",
        "✓ = Unique constraint",
        "PK = Primary Key (auto-increment)",
        "FK = Foreign Key (with cascade)",
        "Enum = Predefined values only",
        "JSON = Flexible data structure"
    ]
    
    y_pos = 1.8
    for constraint in constraints:
        style = 'bold' if constraint.endswith(':') else 'normal'
        ax.text(1, y_pos, constraint, ha='left', va='center', fontsize=9, 
               fontweight=style, color='#374151')
        y_pos -= 0.2
    
    plt.tight_layout()
    return fig

def draw_detailed_model_box(ax, model_name, details):
    """Draw detailed model box with better formatting"""
    x, y = details['pos']
    width, height = details['size']
    color = details['color']
    
    # Main box with shadow effect
    shadow = FancyBboxPatch((x - width/2 + 0.05, y - height/2 - 0.05), width, height,
                           boxstyle="round,pad=0.02", 
                           facecolor='#00000020', alpha=0.3)
    ax.add_patch(shadow)
    
    box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                        boxstyle="round,pad=0.02", 
                        facecolor=color, alpha=0.9, 
                        edgecolor='#1F2937', linewidth=1.8)
    ax.add_patch(box)
    
    # Calculate positioning
    text_y_start = y + height/2 - 0.18
    line_height = 0.14
    
    # Model name with better styling
    ax.text(x, text_y_start, model_name, ha='center', va='center', 
            fontsize=12, fontweight='bold', color='white')
    
    # Separator
    sep_y = text_y_start - 0.1
    ax.plot([x - width/2 + 0.15, x + width/2 - 0.15], [sep_y, sep_y], 
            color='white', linewidth=1.5, alpha=0.9)
    
    # Attributes
    current_y = sep_y - 0.18
    for attr in details['attributes']:
        if current_y > y - height/2 + 0.15:
            ax.text(x - width/2 + 0.12, current_y, attr, 
                   ha='left', va='center', fontsize=8.5, color='white',
                   fontfamily='monospace', fontweight='normal')
            current_y -= line_height
    
    # Method separator
    if details['methods'] and current_y > y - height/2 + 0.15:
        method_sep_y = current_y + 0.07
        ax.plot([x - width/2 + 0.15, x + width/2 - 0.15], [method_sep_y, method_sep_y], 
                color='white', linewidth=1.5, alpha=0.9)
        current_y = method_sep_y - 0.12
    
    # Methods
    for method in details['methods']:
        if current_y > y - height/2 + 0.15:
            ax.text(x - width/2 + 0.12, current_y, method, 
                   ha='left', va='center', fontsize=8.5, color='white',
                   fontfamily='monospace', fontweight='normal')
            current_y -= line_height

def draw_detailed_relationship(ax, source_class, target_class, rel_type, mult1, mult2, label):
    """Draw relationship with enhanced styling"""
    x1, y1 = source_class['pos']
    x2, y2 = target_class['pos']
    w1, h1 = source_class['size']
    w2, h2 = target_class['size']
    
    # Calculate connection points
    if abs(x2 - x1) > abs(y2 - y1):
        if x2 > x1:
            conn_x1, conn_y1 = x1 + w1/2, y1
            conn_x2, conn_y2 = x2 - w2/2, y2
        else:
            conn_x1, conn_y1 = x1 - w1/2, y1
            conn_x2, conn_y2 = x2 + w2/2, y2
    else:
        if y2 > y1:
            conn_x1, conn_y1 = x1, y1 + h1/2
            conn_x2, conn_y2 = x2, y2 - h2/2
        else:
            conn_x1, conn_y1 = x1, y1 - h1/2
            conn_x2, conn_y2 = x2, y2 + h2/2
    
    # Draw relationship
    if rel_type == 'composition':
        ax.annotate('', xy=(conn_x2, conn_y2), xytext=(conn_x1, conn_y1),
                   arrowprops=dict(arrowstyle='->', color='#1F2937', lw=2))
        diamond = patches.RegularPolygon((conn_x1, conn_y1), 4, radius=0.1, 
                                       orientation=np.pi/4, facecolor='#1F2937')
        ax.add_patch(diamond)
    else:
        ax.annotate('', xy=(conn_x2, conn_y2), xytext=(conn_x1, conn_y1),
                   arrowprops=dict(arrowstyle='->', color='#374151', lw=1.5))
    
    # Add labels with better styling
    if mult1:
        ax.text(conn_x1, conn_y1 + 0.2, mult1, ha='center', va='center', 
               fontsize=9, fontweight='bold', color='#1F2937',
               bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.9))
    if mult2:
        ax.text(conn_x2, conn_y2 + 0.2, mult2, ha='center', va='center', 
               fontsize=9, fontweight='bold', color='#1F2937',
               bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.9))
    
    if label:
        mid_x = (conn_x1 + conn_x2) / 2
        mid_y = (conn_y1 + conn_y2) / 2
        ax.text(mid_x, mid_y - 0.2, label, ha='center', va='center', 
               fontsize=8, style='italic', color='#374151',
               bbox=dict(boxstyle="round,pad=0.15", facecolor='white', alpha=0.95,
                        edgecolor='#D1D5DB'))

def main():
    """Generate clear, readable class diagrams"""
    print("Generating Clear AutoGuardian Class Diagrams...")
    
    # Generate main clear class diagram
    print("Creating clear comprehensive class diagram...")
    fig1 = create_clear_class_diagram()
    output_path1 = r"C:\Users\chan-shinan\Documents\icbt\final project\shinan_final_project\autoguardian-fuel-system\AutoGuardian_Clear_Class_Diagram.png"
    fig1.savefig(output_path1, dpi=300, bbox_inches='tight', 
                 facecolor='white', edgecolor='none')
    print(f"Clear class diagram saved to: {output_path1}")
    
    # Generate detailed backend diagram
    print("Creating detailed backend models diagram...")
    fig2 = create_backend_focus_diagram()
    output_path2 = r"C:\Users\chan-shinan\Documents\icbt\final project\shinan_final_project\autoguardian-fuel-system\AutoGuardian_Backend_Clear_Models.png"
    fig2.savefig(output_path2, dpi=300, bbox_inches='tight', 
                 facecolor='white', edgecolor='none')
    print(f"Backend models diagram saved to: {output_path2}")
    
    print("\n[SUCCESS] Clear class diagrams generated!")
    print("\nImprovements made:")
    print("- Larger, clearer text with better font sizes")
    print("- Improved color contrast and readability")
    print("- Better spacing and layout")
    print("- Enhanced visual hierarchy")
    print("- Clearer relationship lines and labels")
    print("- Simplified content for better focus")
    
    # Close figures
    plt.close('all')

if __name__ == "__main__":
    main()