#!/usr/bin/env python3
"""
AutoGuardian Fuel Management System - Class Diagram Generator
This script generates a comprehensive UML class diagram showing all classes,
their attributes (public/private), methods, and relationships.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch, Arrow
import matplotlib.pyplot as plt
import numpy as np

def create_class_diagram():
    """Generate comprehensive UML class diagram with proper UML notation"""
    
    # Create large figure for comprehensive diagram
    fig, ax = plt.subplots(1, 1, figsize=(24, 16))
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 16)
    ax.axis('off')
    
    # Define colors for different types of classes
    colors = {
        'model': '#3B82F6',        # Blue - Database Models
        'service': '#10B981',      # Green - Service Classes
        'ai': '#8B5CF6',          # Purple - AI/ML Classes
        'frontend': '#F59E0B',     # Orange - Frontend Components
        'api': '#EF4444',         # Red - API/Controller Classes
        'config': '#6B7280',      # Gray - Configuration Classes
        'utility': '#EC4899',     # Pink - Utility Classes
        'background': '#F8FAFC'   # Light gray background
    }
    
    # Set background
    ax.add_patch(patches.Rectangle((0, 0), 24, 16, facecolor=colors['background'], alpha=0.3))
    
    # Title
    ax.text(12, 15.5, 'AutoGuardian Fuel Management System', 
            ha='center', va='center', fontsize=24, fontweight='bold')
    ax.text(12, 15, 'Comprehensive UML Class Diagram', 
            ha='center', va='center', fontsize=16, style='italic')
    
    # Define class positions and details
    classes = {
        # ====== DATABASE MODELS LAYER ======
        'User': {
            'pos': (2, 13),
            'size': (2.5, 1.8),
            'color': colors['model'],
            'attributes': [
                '+id: Integer',
                '+username: String(50)',
                '+email: String(100)',
                '+first_name: String(50)',
                '+last_name: String(50)',
                '+phone: String(20)',
                '+is_active: Boolean',
                '+created_at: DateTime',
                '+updated_at: DateTime',
                '-password_hash: String(255)'
            ],
            'methods': [
                '+__init__(username, email, password, ...)',
                '+set_password(password): void',
                '+check_password(password): Boolean',
                '+generate_tokens(): Dict',
                '+to_dict(): Dict',
                '+full_name: String',
                '+vehicle_count: Integer'
            ]
        },
        
        'Vehicle': {
            'pos': (5.5, 13),
            'size': (2.8, 2.2),
            'color': colors['model'],
            'attributes': [
                '+id: Integer',
                '+user_id: Integer',
                '+vehicle_name: String(100)',
                '+make: String(50)',
                '+model: String(50)',
                '+year: Integer',
                '+vehicle_class: String(50)',
                '+engine_size: Numeric(3,1)',
                '+cylinders: Integer',
                '+transmission: String(20)',
                '+fuel_type: String(20)',
                '+tank_capacity: Numeric(5,2)',
                '+is_active: Boolean',
                '+created_at: DateTime'
            ],
            'methods': [
                '+__init__(user_id, vehicle_name, ...)',
                '+display_name: String',
                '+current_odometer: Integer',
                '+get_ml_prediction_features(): Dict',
                '+calculate_average_consumption(): Float',
                '+to_dict(): Dict'
            ]
        },
        
        'FuelRecord': {
            'pos': (9, 13),
            'size': (2.8, 2.2),
            'color': colors['model'],
            'attributes': [
                '+id: Integer',
                '+vehicle_id: Integer',
                '+record_date: Date',
                '+record_time: Time',
                '+existing_tank_percentage: Numeric',
                '+after_refuel_percentage: Numeric',
                '+odo_meter_current_value: Integer',
                '+driving_type: Enum',
                '+location: String(100)',
                '+fuel_price: Numeric(6,2)',
                '+calculated_fuel_added: Numeric',
                '+total_cost: Numeric(8,2)',
                '+notes: Text'
            ],
            'methods': [
                '+__init__(vehicle_id, record_date, ...)',
                '-_calculate_fuel_metrics(): void',
                '+get_previous_record(): FuelRecord',
                '+validate_odometer(): Tuple',
                '+recalculate_metrics(): void',
                '+to_dict(): Dict'
            ]
        },
        
        'AIRecommendation': {
            'pos': (12.5, 13),
            'size': (3, 2.2),
            'color': colors['model'],
            'attributes': [
                '+id: Integer',
                '+user_id: Integer',
                '+vehicle_id: Integer',
                '+recommendation_type: String(20)',
                '+recommendation_title: String(200)',
                '+recommendation_text: Text',
                '+performance_analysis: Text',
                '+priority_level: String(20)',
                '+category: String(50)',
                '+impact_score: Numeric(3,2)',
                '+is_read: Boolean',
                '+confidence_level: Numeric(3,2)',
                '+created_at: DateTime'
            ],
            'methods': [
                '+__init__(user_id, vehicle_id, ...)',
                '+is_expired: Boolean',
                '+mark_as_read(): void',
                '+mark_as_implemented(): void',
                '+calculate_potential_savings(): Dict',
                '+to_dict(): Dict'
            ]
        },
        
        'VehicleSale': {
            'pos': (16.5, 13),
            'size': (2.5, 1.8),
            'color': colors['model'],
            'attributes': [
                '+id: Integer',
                '+user_id: Integer',
                '+vehicle_id: Integer',
                '+selling_price: Float',
                '+features: JSON',
                '+description: Text',
                '+is_active: Boolean',
                '+is_sold: Boolean',
                '+created_at: DateTime',
                '-minimum_price: Float'
            ],
            'methods': [
                '+__init__(user_id, vehicle_id, ...)',
                '+to_dict(): Dict',
                '+update_sale(): void',
                '+deactivate_sale(): void',
                '+mark_as_sold(): void'
            ]
        },
        
        'Negotiation': {
            'pos': (20, 13),
            'size': (2.5, 1.8),
            'color': colors['model'],
            'attributes': [
                '+id: Integer',
                '+vehicle_sale_id: Integer',
                '+buyer_name: String(100)',
                '+buyer_email: String(150)',
                '+buyer_contact: String(20)',
                '+final_offer: Float',
                '+chat_history: JSON',
                '+status: String(20)',
                '+created_at: DateTime'
            ],
            'methods': [
                '+__init__(vehicle_sale_id, ...)',
                '+to_dict(): Dict',
                '+update_status(): void',
                '+add_chat_message(): void'
            ]
        },
        
        # ====== SERVICE LAYER ======
        'FuelConsumptionPredictor': {
            'pos': (2, 10),
            'size': (3, 2),
            'color': colors['ai'],
            'attributes': [
                '-model_path: String',
                '-model: ML_Model',
                '-is_loaded: Boolean'
            ],
            'methods': [
                '+__init__(model_path): void',
                '+load_model(): Boolean',
                '+preprocess_features(): Dict',
                '-_extract_engine_size(): Float',
                '-_map_transmission(): String',
                '+predict(vehicle_data): Dict',
                '-_estimate_emissions(): Float',
                '+predict_multiple(): List[Dict]',
                '+validate_input(): Tuple'
            ]
        },
        
        'GenAIRecommendationService': {
            'pos': (6, 10),
            'size': (3.2, 2),
            'color': colors['ai'],
            'attributes': [
                '-api_key: String',
                '-model: GenAI_Model',
                '-is_configured: Boolean'
            ],
            'methods': [
                '+__init__(api_key): void',
                '+configure_genai(): void',
                '+generate_maintenance_recommendation(): Dict',
                '+generate_efficiency_recommendation(): Dict',
                '-_create_maintenance_prompt(): String',
                '-_create_efficiency_prompt(): String',
                '-_parse_maintenance_response(): Dict',
                '-_fallback_recommendation(): Dict',
                '+test_connection(): Dict'
            ]
        },
        
        'NegotiationBot': {
            'pos': (10.5, 10),
            'size': (3, 2),
            'color': colors['service'],
            'attributes': [
                '-base_negotiation_steps: List[Float]',
                '-genai_service: GenAIService',
                '-use_ai: Boolean',
                '-positive_responses: List[String]'
            ],
            'methods': [
                '+__init__(): void',
                '+extract_price_from_message(): Float',
                '+generate_ai_response(): String',
                '-_get_situation_context(): String',
                '+analyze_message_intent(): Dict',
                '+calculate_counter_offer(): Float',
                '+generate_response(): Tuple',
                '+parse_contact_details(): Dict'
            ]
        },
        
        'FeatureProcessor': {
            'pos': (14.5, 10),
            'size': (3, 2),
            'color': colors['utility'],
            'attributes': [
                '-vehicle_class_mapping: Dict',
                '-make_standardization: Dict',
                '-model_standardization: Dict'
            ],
            'methods': [
                '+__init__(): void',
                '-_create_vehicle_class_mapping(): Dict',
                '+standardize_make(): String',
                '+standardize_model(): String',
                '+standardize_vehicle_class(): String',
                '+extract_numeric_engine_size(): Float',
                '+process_vehicle_features(): Dict',
                '+validate_processed_features(): Tuple'
            ]
        },
        
        # ====== FRONTEND COMPONENTS ======
        'AuthService': {
            'pos': (2, 6.5),
            'size': (2.5, 1.8),
            'color': colors['frontend'],
            'attributes': [
                '+baseURL: String',
                '+endpoints: Object'
            ],
            'methods': [
                '+login(credentials): Promise<AuthResponse>',
                '+register(userData): Promise<AuthResponse>',
                '+logout(): void',
                '+getCurrentUser(): User',
                '+isAuthenticated(): Boolean',
                '+getToken(): String'
            ]
        },
        
        'ApiService': {
            'pos': (5.5, 6.5),
            'size': (3, 2.2),
            'color': colors['frontend'],
            'attributes': [
                '+baseURL: String',
                '+authToken: String'
            ],
            'methods': [
                '+registerVehicle(): Promise<Vehicle>',
                '+getVehicles(): Promise<Vehicle[]>',
                '+addFuelRecord(): Promise<FuelRecord>',
                '+getFuelRecords(): Promise<FuelRecord[]>',
                '+generateMLPrediction(): Promise<Prediction>',
                '+generateAIRecommendation(): Promise<Recommendation>',
                '+getDashboardAnalytics(): Promise<Analytics>',
                '+createVehicleSale(): Promise<VehicleSale>',
                '+startNegotiation(): Promise<Negotiation>',
                '+continueNegotiation(): Promise<NegotiationResponse>'
            ]
        },
        
        'Dashboard': {
            'pos': (9.5, 6.5),
            'size': (2.5, 1.8),
            'color': colors['frontend'],
            'attributes': [
                '+analytics: DashboardAnalytics',
                '+isLoading: Boolean',
                '+selectedPeriod: String'
            ],
            'methods': [
                '+useEffect(): void',
                '+fetchAnalytics(): Promise<void>',
                '+handlePeriodChange(): void',
                '+renderCharts(): JSX.Element',
                '+render(): JSX.Element'
            ]
        },
        
        'VehiclesPage': {
            'pos': (13, 6.5),
            'size': (2.5, 1.8),
            'color': colors['frontend'],
            'attributes': [
                '+vehicles: Vehicle[]',
                '+isLoading: Boolean',
                '+showModal: Boolean',
                '+formData: Partial<Vehicle>'
            ],
            'methods': [
                '+useEffect(): void',
                '+fetchVehicles(): Promise<void>',
                '+handleSubmit(): Promise<void>',
                '+handleDelete(): Promise<void>',
                '+render(): JSX.Element'
            ]
        },
        
        'AIInsightsPage': {
            'pos': (16.5, 6.5),
            'size': (2.8, 1.8),
            'color': colors['frontend'],
            'attributes': [
                '+predictions: MLPrediction[]',
                '+recommendations: AIRecommendation[]',
                '+selectedVehicle: Vehicle',
                '+isLoading: Boolean'
            ],
            'methods': [
                '+useEffect(): void',
                '+fetchPredictions(): Promise<void>',
                '+generateNewPrediction(): Promise<void>',
                '+handleVehicleSelect(): void',
                '+render(): JSX.Element'
            ]
        },
        
        'MarketplacePage': {
            'pos': (20, 6.5),
            'size': (2.5, 1.8),
            'color': colors['frontend'],
            'attributes': [
                '+vehicleSales: VehicleSale[]',
                '+filters: Object',
                '+selectedVehicle: VehicleSale',
                '+showNegotiation: Boolean'
            ],
            'methods': [
                '+useEffect(): void',
                '+fetchVehicleSales(): Promise<void>',
                '+handleFilterChange(): void',
                '+startNegotiation(): Promise<void>',
                '+render(): JSX.Element'
            ]
        },
        
        # ====== CONFIGURATION & UTILITIES ======
        'Config': {
            'pos': (18, 10),
            'size': (2.5, 1.8),
            'color': colors['config'],
            'attributes': [
                '+SECRET_KEY: String',
                '+SQLALCHEMY_DATABASE_URI: String',
                '+JWT_SECRET_KEY: String',
                '+JWT_ACCESS_TOKEN_EXPIRES: timedelta',
                '+GOOGLE_AI_API_KEY: String',
                '+BCRYPT_LOG_ROUNDS: Integer',
                '+ML_MODEL_PATH: String'
            ],
            'methods': [
                '+__init__(): void'
            ]
        },
        
        'Validators': {
            'pos': (21.5, 10),
            'size': (2, 1.5),
            'color': colors['utility'],
            'attributes': [],
            'methods': [
                '+validate_email(): Boolean',
                '+validate_password(): List[String]',
                '+validate_vehicle_id(): Boolean',
                '+validate_fuel_record(): List[String]',
                '+sanitize_string(): String',
                '+validate_pagination(): List[String]'
            ]
        }
    }
    
    # Draw all classes
    for class_name, details in classes.items():
        draw_class_box(ax, class_name, details)
    
    # Define relationships with proper UML notation
    relationships = [
        # Model Relationships (Database FK relationships)
        ('User', 'Vehicle', 'composition', '1', '*', 'owns'),
        ('User', 'AIRecommendation', 'composition', '1', '*', 'receives'),
        ('User', 'VehicleSale', 'composition', '1', '*', 'sells'),
        ('Vehicle', 'FuelRecord', 'composition', '1', '*', 'has'),
        ('Vehicle', 'AIRecommendation', 'association', '1', '*', 'generates'),
        ('VehicleSale', 'Negotiation', 'composition', '1', '*', 'negotiates'),
        
        # Service Dependencies
        ('FuelConsumptionPredictor', 'FeatureProcessor', 'dependency', '', '', 'uses'),
        ('NegotiationBot', 'GenAIRecommendationService', 'dependency', '', '', 'uses'),
        ('GenAIRecommendationService', 'AIRecommendation', 'dependency', '', '', 'creates'),
        ('FuelConsumptionPredictor', 'Vehicle', 'dependency', '', '', 'analyzes'),
        
        # Frontend to Service relationships
        ('AuthService', 'User', 'dependency', '', '', 'authenticates'),
        ('ApiService', 'Vehicle', 'dependency', '', '', 'manages'),
        ('ApiService', 'FuelRecord', 'dependency', '', '', 'tracks'),
        ('ApiService', 'AIRecommendation', 'dependency', '', '', 'requests'),
        ('ApiService', 'VehicleSale', 'dependency', '', '', 'lists'),
        
        # Frontend Component Dependencies
        ('Dashboard', 'ApiService', 'dependency', '', '', 'uses'),
        ('VehiclesPage', 'ApiService', 'dependency', '', '', 'uses'),
        ('AIInsightsPage', 'ApiService', 'dependency', '', '', 'uses'),
        ('MarketplacePage', 'ApiService', 'dependency', '', '', 'uses'),
        ('AuthService', 'ApiService', 'dependency', '', '', 'configures'),
        
        # Configuration Dependencies
        ('GenAIRecommendationService', 'Config', 'dependency', '', '', 'configures'),
        ('FuelConsumptionPredictor', 'Config', 'dependency', '', '', 'configures'),
    ]
    
    # Draw relationships
    for source, target, rel_type, multiplicity1, multiplicity2, label in relationships:
        if source in classes and target in classes:
            draw_relationship(ax, classes[source], classes[target], rel_type, 
                            multiplicity1, multiplicity2, label)
    
    # Add layer labels
    ax.text(0.5, 14, 'DATABASE\nMODELS', ha='center', va='center', 
            fontsize=12, fontweight='bold', rotation=90, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor=colors['model'], alpha=0.7))
    
    ax.text(0.5, 11, 'SERVICE\nLAYER', ha='center', va='center', 
            fontsize=12, fontweight='bold', rotation=90,
            bbox=dict(boxstyle="round,pad=0.3", facecolor=colors['service'], alpha=0.7))
    
    ax.text(0.5, 7.5, 'FRONTEND\nCOMPONENTS', ha='center', va='center', 
            fontsize=12, fontweight='bold', rotation=90,
            bbox=dict(boxstyle="round,pad=0.3", facecolor=colors['frontend'], alpha=0.7))
    
    # Add legend
    legend_elements = [
        patches.Rectangle((0, 0), 1, 1, facecolor=colors['model'], alpha=0.7, label='Database Models'),
        patches.Rectangle((0, 0), 1, 1, facecolor=colors['service'], alpha=0.7, label='Service Classes'),
        patches.Rectangle((0, 0), 1, 1, facecolor=colors['ai'], alpha=0.7, label='AI/ML Services'),
        patches.Rectangle((0, 0), 1, 1, facecolor=colors['frontend'], alpha=0.7, label='Frontend Components'),
        patches.Rectangle((0, 0), 1, 1, facecolor=colors['config'], alpha=0.7, label='Configuration'),
        patches.Rectangle((0, 0), 1, 1, facecolor=colors['utility'], alpha=0.7, label='Utilities'),
    ]
    
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0.02, 0.98), fontsize=10)
    
    # Add relationship legend
    ax.text(0.5, 3.5, 'Relationships:', fontsize=12, fontweight='bold')
    ax.text(0.5, 3.2, '──── Association', fontsize=10)
    ax.text(0.5, 2.9, '♦──── Composition', fontsize=10)
    ax.text(0.5, 2.6, '- - -> Dependency', fontsize=10)
    ax.text(0.5, 2.3, '1, * Multiplicity', fontsize=10)
    
    # Add UML notation legend
    ax.text(0.5, 1.8, 'UML Notation:', fontsize=12, fontweight='bold')
    ax.text(0.5, 1.5, '+ Public attribute/method', fontsize=10)
    ax.text(0.5, 1.2, '- Private attribute/method', fontsize=10)
    ax.text(0.5, 0.9, '# Protected attribute/method', fontsize=10)
    
    plt.tight_layout()
    return fig

def draw_class_box(ax, class_name, details):
    """Draw a UML class box with attributes and methods"""
    x, y = details['pos']
    width, height = details['size']
    color = details['color']
    
    # Main class box
    box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                        boxstyle="round,pad=0.02", 
                        facecolor=color, alpha=0.8, 
                        edgecolor='black', linewidth=1.2)
    ax.add_patch(box)
    
    # Calculate text positioning
    text_y_start = y + height/2 - 0.15
    line_height = 0.1
    
    # Class name (bold)
    ax.text(x, text_y_start, class_name, ha='center', va='center', 
            fontsize=10, fontweight='bold', color='white')
    
    # Separator line after class name
    ax.plot([x - width/2 + 0.05, x + width/2 - 0.05], 
            [text_y_start - 0.08, text_y_start - 0.08], 
            color='white', linewidth=1)
    
    # Attributes section
    current_y = text_y_start - 0.18
    for attr in details['attributes']:
        if current_y > y - height/2 + 0.05:  # Check if we have space
            ax.text(x - width/2 + 0.05, current_y, attr, 
                   ha='left', va='center', fontsize=7, color='white')
            current_y -= line_height
    
    # Separator line after attributes (if we have methods)
    if details['methods'] and current_y > y - height/2 + 0.05:
        ax.plot([x - width/2 + 0.05, x + width/2 - 0.05], 
                [current_y + 0.05, current_y + 0.05], 
                color='white', linewidth=1)
        current_y -= 0.05
    
    # Methods section
    for method in details['methods']:
        if current_y > y - height/2 + 0.05:  # Check if we have space
            ax.text(x - width/2 + 0.05, current_y, method, 
                   ha='left', va='center', fontsize=7, color='white')
            current_y -= line_height

def draw_relationship(ax, source_class, target_class, rel_type, mult1, mult2, label):
    """Draw relationship between two classes with UML notation"""
    x1, y1 = source_class['pos']
    x2, y2 = target_class['pos']
    
    # Calculate connection points (edge of boxes)
    w1, h1 = source_class['size']
    w2, h2 = target_class['size']
    
    # Determine connection points
    if abs(x2 - x1) > abs(y2 - y1):  # Horizontal connection
        if x2 > x1:  # Target is to the right
            conn_x1, conn_y1 = x1 + w1/2, y1
            conn_x2, conn_y2 = x2 - w2/2, y2
        else:  # Target is to the left
            conn_x1, conn_y1 = x1 - w1/2, y1
            conn_x2, conn_y2 = x2 + w2/2, y2
    else:  # Vertical connection
        if y2 > y1:  # Target is above
            conn_x1, conn_y1 = x1, y1 + h1/2
            conn_x2, conn_y2 = x2, y2 - h2/2
        else:  # Target is below
            conn_x1, conn_y1 = x1, y1 - h1/2
            conn_x2, conn_y2 = x2, y2 + h2/2
    
    # Draw relationship line based on type
    if rel_type == 'composition':
        # Composition: filled diamond at source end
        ax.annotate('', xy=(conn_x2, conn_y2), xytext=(conn_x1, conn_y1),
                   arrowprops=dict(arrowstyle='->', color='black', lw=1.2))
        # Add diamond at source
        diamond_size = 0.08
        diamond = patches.RegularPolygon((conn_x1, conn_y1), 4, radius=diamond_size, 
                                       orientation=np.pi/4, facecolor='black')
        ax.add_patch(diamond)
        
    elif rel_type == 'association':
        # Association: simple line with arrow
        ax.annotate('', xy=(conn_x2, conn_y2), xytext=(conn_x1, conn_y1),
                   arrowprops=dict(arrowstyle='->', color='black', lw=1))
        
    elif rel_type == 'dependency':
        # Dependency: dashed line with arrow
        ax.annotate('', xy=(conn_x2, conn_y2), xytext=(conn_x1, conn_y1),
                   arrowprops=dict(arrowstyle='->', color='black', lw=1, linestyle='dashed'))
    
    # Add multiplicity labels
    if mult1:
        ax.text(conn_x1, conn_y1 + 0.15, mult1, ha='center', va='center', 
               fontsize=8, fontweight='bold')
    if mult2:
        ax.text(conn_x2, conn_y2 + 0.15, mult2, ha='center', va='center', 
               fontsize=8, fontweight='bold')
    
    # Add relationship label at midpoint
    if label:
        mid_x = (conn_x1 + conn_x2) / 2
        mid_y = (conn_y1 + conn_y2) / 2
        ax.text(mid_x, mid_y + 0.1, label, ha='center', va='center', 
               fontsize=7, style='italic',
               bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))

def create_detailed_backend_class_diagram():
    """Create a focused diagram showing just the backend models with full detail"""
    
    fig, ax = plt.subplots(1, 1, figsize=(20, 14))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # Title
    ax.text(10, 13.5, 'AutoGuardian Backend - Database Models Detail', 
            ha='center', va='center', fontsize=20, fontweight='bold')
    ax.text(10, 13, 'Complete Class Diagram with All Attributes and Methods', 
            ha='center', va='center', fontsize=14, style='italic')
    
    # Define detailed backend classes
    backend_classes = {
        'User': {
            'pos': (3, 10),
            'size': (3.5, 3.5),
            'color': '#3B82F6',
            'attributes': [
                '+id: Integer (PK)',
                '+username: String(50) (Unique)',
                '+email: String(100) (Unique)',
                '+first_name: String(50)',
                '+last_name: String(50)',
                '+phone: String(20)',
                '+is_active: Boolean',
                '+created_at: DateTime',
                '+updated_at: DateTime',
                '-password_hash: String(255)'
            ],
            'methods': [
                '+__init__(username, email, password, ...)',
                '+set_password(password): void',
                '+check_password(password): Boolean',
                '+generate_tokens(): Dict',
                '+to_dict(include_sensitive=False): Dict',
                '@property +full_name: String',
                '@property +vehicle_count: Integer',
                '@classmethod +find_by_username(username): User',
                '@classmethod +find_by_email(email): User'
            ]
        },
        
        'Vehicle': {
            'pos': (8.5, 10),
            'size': (4, 4),
            'color': '#3B82F6',
            'attributes': [
                '+id: Integer (PK)',
                '+user_id: Integer (FK)',
                '+vehicle_name: String(100)',
                '+make: String(50)',
                '+model: String(50)',
                '+year: Integer',
                '+vehicle_class: String(50)',
                '+engine_size: Numeric(3,1)',
                '+cylinders: Integer',
                '+transmission: String(20)',
                '+fuel_type: String(20)',
                '+tank_capacity: Numeric(5,2)',
                '+starting_odometer_value: Integer',
                '+is_active: Boolean',
                '+created_at: DateTime'
            ],
            'methods': [
                '+__init__(user_id, vehicle_name, ...)',
                '@property +display_name: String',
                '@property +current_odometer: Integer',
                '@property +total_distance_driven: Integer',
                '+get_ml_prediction_features(): Dict',
                '+calculate_average_consumption(): Float',
                '+get_consumption_by_driving_type(): Dict',
                '+to_dict(include_stats=True): Dict',
                '@classmethod +find_by_user(user_id): List[Vehicle]'
            ]
        },
        
        'FuelRecord': {
            'pos': (14, 10),
            'size': (4.5, 4),
            'color': '#3B82F6',
            'attributes': [
                '+id: Integer (PK)',
                '+vehicle_id: Integer (FK)',
                '+record_date: Date',
                '+record_time: Time',
                '+existing_tank_percentage: Numeric(5,2)',
                '+after_refuel_percentage: Numeric(5,2)',
                '+odo_meter_current_value: Integer',
                '+driving_type: Enum(\'city\', \'highway\', \'mix\')',
                '+location: String(100)',
                '+fuel_price: Numeric(6,2)',
                '+calculated_fuel_added: Numeric(6,2)',
                '+total_cost: Numeric(8,2)',
                '+km_driven_since_last: Integer',
                '+actual_consumption_l_100km: Numeric(6,2)',
                '+notes: Text'
            ],
            'methods': [
                '+__init__(vehicle_id, record_date, ...)',
                '-_calculate_fuel_metrics(): void',
                '+get_previous_record(): FuelRecord',
                '@property +datetime: DateTime',
                '@property +fuel_efficiency_rating: String',
                '+validate_odometer(): Tuple[Boolean, String]',
                '+recalculate_metrics(): void',
                '+to_dict(include_analysis=False): Dict',
                '@classmethod +get_vehicle_records(...): List[FuelRecord]'
            ]
        },
        
        'AIRecommendation': {
            'pos': (3, 5),
            'size': (4.2, 3.5),
            'color': '#8B5CF6',
            'attributes': [
                '+id: Integer (PK)',
                '+user_id: Integer (FK)',
                '+vehicle_id: Integer (FK)',
                '+recommendation_type: String(20)',
                '+recommendation_title: String(200)',
                '+recommendation_text: Text',
                '+performance_analysis: Text',
                '+priority_level: String(20)',
                '+category: String(50)',
                '+impact_score: Numeric(3,2)',
                '+is_read: Boolean',
                '+confidence_level: Numeric(3,2)',
                '+ai_model_used: String(50)',
                '+created_at: DateTime',
                '+expires_at: DateTime'
            ],
            'methods': [
                '+__init__(user_id, vehicle_id, ...)',
                '@property +is_expired: Boolean',
                '@property +priority_color: String',
                '+mark_as_read(): void',
                '+mark_as_implemented(notes): void',
                '+calculate_potential_savings(): Dict',
                '+to_dict(include_full_text=True): Dict',
                '@classmethod +get_user_recommendations(...): List[AIRecommendation]'
            ]
        },
        
        'VehicleSale': {
            'pos': (9, 5),
            'size': (3.5, 3),
            'color': '#10B981',
            'attributes': [
                '+id: Integer (PK)',
                '+user_id: Integer (FK)',
                '+vehicle_id: Integer (FK)',
                '+selling_price: Float',
                '+features: JSON',
                '+description: Text',
                '+is_active: Boolean',
                '+is_sold: Boolean',
                '+created_at: DateTime',
                '-minimum_price: Float'
            ],
            'methods': [
                '+__init__(user_id, vehicle_id, ...)',
                '+to_dict(include_sensitive=False): Dict',
                '+update_sale(**kwargs): void',
                '+deactivate_sale(): void',
                '+mark_as_sold(): void',
                '@classmethod +get_active_sales(...): List[VehicleSale]',
                '@classmethod +get_user_sales(user_id): List[VehicleSale]'
            ]
        },
        
        'Negotiation': {
            'pos': (14.5, 5),
            'size': (3.5, 3),
            'color': '#10B981',
            'attributes': [
                '+id: Integer (PK)',
                '+vehicle_sale_id: Integer (FK)',
                '+buyer_name: String(100)',
                '+buyer_email: String(150)',
                '+buyer_contact: String(20)',
                '+final_offer: Float',
                '+chat_history: JSON',
                '+status: String(20)',
                '+created_at: DateTime'
            ],
            'methods': [
                '+__init__(vehicle_sale_id, ...)',
                '+to_dict(): Dict',
                '+update_status(status): void',
                '+add_chat_message(sender, message): void',
                '@classmethod +get_sale_negotiations(...): List[Negotiation]'
            ]
        }
    }
    
    # Draw all backend classes
    for class_name, details in backend_classes.items():
        draw_detailed_class_box(ax, class_name, details)
    
    # Define relationships with detailed multiplicity
    detailed_relationships = [
        ('User', 'Vehicle', 'composition', '1', '0..*', 'owns'),
        ('User', 'AIRecommendation', 'composition', '1', '0..*', 'receives'),
        ('User', 'VehicleSale', 'composition', '1', '0..*', 'creates'),
        ('Vehicle', 'FuelRecord', 'composition', '1', '0..*', 'tracks'),
        ('Vehicle', 'AIRecommendation', 'association', '1', '0..*', 'generates for'),
        ('VehicleSale', 'Negotiation', 'composition', '1', '0..*', 'negotiated through'),
    ]
    
    # Draw relationships
    for source, target, rel_type, mult1, mult2, label in detailed_relationships:
        if source in backend_classes and target in backend_classes:
            draw_detailed_relationship(ax, backend_classes[source], backend_classes[target], 
                                     rel_type, mult1, mult2, label)
    
    # Add notes about database constraints
    notes = [
        "Database Constraints:",
        "• All PK fields are auto-increment",
        "• FK fields have cascade delete",
        "• Unique constraints on email/username",
        "• Indexes on frequently queried fields",
        "• Enum constraints on driving_type, priority_level, etc."
    ]
    
    note_y = 1.5
    for note in notes:
        ax.text(1, note_y, note, ha='left', va='center', fontsize=9, 
               fontweight='bold' if note.endswith(':') else 'normal')
        note_y -= 0.2
    
    plt.tight_layout()
    return fig

def draw_detailed_class_box(ax, class_name, details):
    """Draw a detailed UML class box with more spacing and formatting"""
    x, y = details['pos']
    width, height = details['size']
    color = details['color']
    
    # Main class box
    box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                        boxstyle="round,pad=0.02", 
                        facecolor=color, alpha=0.9, 
                        edgecolor='black', linewidth=1.5)
    ax.add_patch(box)
    
    # Calculate text positioning
    text_y_start = y + height/2 - 0.2
    line_height = 0.12
    
    # Class name (bold, larger)
    ax.text(x, text_y_start, class_name, ha='center', va='center', 
            fontsize=12, fontweight='bold', color='white')
    
    # Separator line after class name
    ax.plot([x - width/2 + 0.1, x + width/2 - 0.1], 
            [text_y_start - 0.1, text_y_start - 0.1], 
            color='white', linewidth=1.5)
    
    # Attributes section
    current_y = text_y_start - 0.25
    for attr in details['attributes']:
        if current_y > y - height/2 + 0.1:
            ax.text(x - width/2 + 0.1, current_y, attr, 
                   ha='left', va='center', fontsize=8, color='white', fontweight='normal')
            current_y -= line_height
    
    # Separator line after attributes
    if details['methods'] and current_y > y - height/2 + 0.1:
        ax.plot([x - width/2 + 0.1, x + width/2 - 0.1], 
                [current_y + 0.06, current_y + 0.06], 
                color='white', linewidth=1.5)
        current_y -= 0.1
    
    # Methods section
    for method in details['methods']:
        if current_y > y - height/2 + 0.1:
            ax.text(x - width/2 + 0.1, current_y, method, 
                   ha='left', va='center', fontsize=8, color='white', fontweight='normal')
            current_y -= line_height

def draw_detailed_relationship(ax, source_class, target_class, rel_type, mult1, mult2, label):
    """Draw detailed relationship with proper UML notation"""
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
                   arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
        diamond = patches.RegularPolygon((conn_x1, conn_y1), 4, radius=0.1, 
                                       orientation=np.pi/4, facecolor='black')
        ax.add_patch(diamond)
    else:
        ax.annotate('', xy=(conn_x2, conn_y2), xytext=(conn_x1, conn_y1),
                   arrowprops=dict(arrowstyle='->', color='black', lw=1.2))
    
    # Add multiplicity and labels
    if mult1:
        ax.text(conn_x1, conn_y1 + 0.2, mult1, ha='center', va='center', 
               fontsize=9, fontweight='bold')
    if mult2:
        ax.text(conn_x2, conn_y2 + 0.2, mult2, ha='center', va='center', 
               fontsize=9, fontweight='bold')
    
    if label:
        mid_x = (conn_x1 + conn_x2) / 2
        mid_y = (conn_y1 + conn_y2) / 2
        ax.text(mid_x, mid_y - 0.15, label, ha='center', va='center', 
               fontsize=8, style='italic',
               bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.9))

def main():
    """Generate comprehensive class diagrams"""
    print("Generating AutoGuardian Class Diagrams...")
    
    # Generate comprehensive class diagram
    print("Creating comprehensive UML class diagram...")
    fig1 = create_class_diagram()
    output_path1 = r"C:\Users\chan-shinan\Documents\icbt\final project\shinan_final_project\autoguardian-fuel-system\AutoGuardian_Complete_Class_Diagram.png"
    fig1.savefig(output_path1, dpi=300, bbox_inches='tight', 
                 facecolor='white', edgecolor='none')
    print(f"Complete class diagram saved to: {output_path1}")
    
    # Generate detailed backend diagram
    print("Creating detailed backend models diagram...")
    fig2 = create_detailed_backend_class_diagram()
    output_path2 = r"C:\Users\chan-shinan\Documents\icbt\final project\shinan_final_project\autoguardian-fuel-system\AutoGuardian_Backend_Models_Detailed.png"
    fig2.savefig(output_path2, dpi=300, bbox_inches='tight', 
                 facecolor='white', edgecolor='none')
    print(f"Backend models diagram saved to: {output_path2}")
    
    print("\n[SUCCESS] Class diagrams generated successfully!")
    print("\nDiagrams include:")
    print("1. Complete UML class diagram with all components")
    print("2. Detailed backend database models diagram")
    print("\nFeatures:")
    print("- Proper UML notation with +public/-private attributes/methods")
    print("- Relationship types (composition, association, dependency)")
    print("- Multiplicity indicators (1, *, 0..*, etc.)")
    print("- Color-coded layers (Models, Services, Frontend, etc.)")
    print("- Complete attribute and method listings")
    print("- Database constraints and relationships")
    
    # Close figures to prevent display issues
    plt.close('all')

if __name__ == "__main__":
    main()