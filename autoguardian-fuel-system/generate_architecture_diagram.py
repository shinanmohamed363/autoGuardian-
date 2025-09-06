#!/usr/bin/env python3
"""
AutoGuardian Fuel Management System - Architecture Diagram Generator
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_architecture_diagram():
    """Generate comprehensive system architecture diagram"""
    
    # Create figure and axis
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Define colors
    colors = {
        'frontend': '#3B82F6',      # Blue
        'backend': '#10B981',       # Green  
        'database': '#F59E0B',      # Orange
        'ai': '#8B5CF6',           # Purple
        'external': '#EF4444',      # Red
        'service': '#6B7280',       # Gray
        'background': '#F8FAFC'     # Light gray
    }
    
    # Set background
    ax.add_patch(patches.Rectangle((0, 0), 16, 12, facecolor=colors['background'], alpha=0.3))
    
    # Title
    ax.text(8, 11.5, 'AutoGuardian Fuel Management System', 
            ha='center', va='center', fontsize=20, fontweight='bold')
    ax.text(8, 11, 'System Architecture Overview', 
            ha='center', va='center', fontsize=14, style='italic')
    
    # ===== FRONTEND LAYER =====
    frontend_y = 9.5
    ax.text(2, frontend_y + 0.3, 'Frontend Layer (React TypeScript)', 
            ha='center', fontsize=12, fontweight='bold')
    
    # Frontend components
    frontend_components = [
        ('Landing Page', 0.5, frontend_y),
        ('Dashboard', 2, frontend_y),
        ('Fuel Records', 3.5, frontend_y),
        ('Vehicles', 5, frontend_y),
        ('Marketplace', 6.5, frontend_y),
        ('Seller Dashboard', 8, frontend_y),
        ('AI Insights', 9.5, frontend_y),
    ]
    
    for name, x, y in frontend_components:
        box = FancyBboxPatch((x-0.4, y-0.2), 0.8, 0.4, 
                            boxstyle="round,pad=0.02", 
                            facecolor=colors['frontend'], 
                            alpha=0.7, edgecolor='black', linewidth=0.5)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=8, color='white', fontweight='bold')
    
    # Frontend services
    ax.text(12, frontend_y + 0.3, 'Frontend Services', 
            ha='center', fontsize=10, fontweight='bold')
    
    frontend_services = [
        ('API Service', 11.2, frontend_y),
        ('Auth Service', 12.8, frontend_y),
    ]
    
    for name, x, y in frontend_services:
        box = FancyBboxPatch((x-0.35, y-0.15), 0.7, 0.3, 
                            boxstyle="round,pad=0.02", 
                            facecolor=colors['service'], 
                            alpha=0.7, edgecolor='black', linewidth=0.5)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=7, color='white')
    
    # ===== BACKEND LAYER =====
    backend_y = 7.5
    ax.text(8, backend_y + 0.5, 'Backend Layer (Flask Python)', 
            ha='center', fontsize=12, fontweight='bold')
    
    # API Routes
    ax.text(2, backend_y + 0.2, 'API Routes', ha='center', fontsize=10, fontweight='bold')
    api_routes = [
        ('Auth', 0.7, backend_y),
        ('Vehicles', 1.5, backend_y),
        ('Fuel Records', 2.3, backend_y),
        ('Analytics', 3.1, backend_y),
        ('Vehicle Sales', 3.9, backend_y),
    ]
    
    for name, x, y in api_routes:
        box = FancyBboxPatch((x-0.25, y-0.15), 0.5, 0.3, 
                            boxstyle="round,pad=0.02", 
                            facecolor=colors['backend'], 
                            alpha=0.7, edgecolor='black', linewidth=0.5)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=6, color='white')
    
    # Business Services
    ax.text(7, backend_y + 0.2, 'Business Services', ha='center', fontsize=10, fontweight='bold')
    business_services = [
        ('Negotiation Bot', 6, backend_y),
        ('Fuel Calculator', 7, backend_y),
        ('Prediction Engine', 8, backend_y),
    ]
    
    for name, x, y in business_services:
        box = FancyBboxPatch((x-0.4, y-0.15), 0.8, 0.3, 
                            boxstyle="round,pad=0.02", 
                            facecolor=colors['service'], 
                            alpha=0.7, edgecolor='black', linewidth=0.5)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=6, color='white')
    
    # Authentication & Security
    ax.text(11.5, backend_y + 0.2, 'Security', ha='center', fontsize=10, fontweight='bold')
    security_services = [
        ('JWT Auth', 10.8, backend_y),
        ('Password Hash', 11.5, backend_y),
        ('Validators', 12.2, backend_y),
    ]
    
    for name, x, y in security_services:
        box = FancyBboxPatch((x-0.25, y-0.15), 0.5, 0.3, 
                            boxstyle="round,pad=0.02", 
                            facecolor=colors['service'], 
                            alpha=0.8, edgecolor='black', linewidth=0.5)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=6, color='white')
    
    # ===== AI SERVICES LAYER =====
    ai_y = 6
    ax.text(3, ai_y + 0.3, 'AI Services Layer', 
            ha='center', fontsize=12, fontweight='bold')
    
    ai_services = [
        ('GenAI Service\n(Gemini 2.0)', 2, ai_y),
        ('Intent Analysis', 3.5, ai_y),
        ('Price Negotiation', 5, ai_y),
        ('Fuel Recommendations', 6.5, ai_y),
    ]
    
    for name, x, y in ai_services:
        box = FancyBboxPatch((x-0.5, y-0.2), 1, 0.4, 
                            boxstyle="round,pad=0.02", 
                            facecolor=colors['ai'], 
                            alpha=0.7, edgecolor='black', linewidth=0.5)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=7, color='white', fontweight='bold')
    
    # ===== DATA LAYER =====
    data_y = 4
    ax.text(3, data_y + 0.5, 'Data Layer', 
            ha='center', fontsize=12, fontweight='bold')
    
    # Database Models
    ax.text(3, data_y + 0.2, 'Database Models (SQLAlchemy ORM)', ha='center', fontsize=10, fontweight='bold')
    db_models = [
        ('User', 1, data_y),
        ('Vehicle', 2, data_y),
        ('Fuel Record', 3, data_y),
        ('Vehicle Sale', 4, data_y),
        ('Negotiation', 5, data_y),
        ('Predictions', 6, data_y),
    ]
    
    for name, x, y in db_models:
        box = FancyBboxPatch((x-0.35, y-0.15), 0.7, 0.3, 
                            boxstyle="round,pad=0.02", 
                            facecolor=colors['database'], 
                            alpha=0.7, edgecolor='black', linewidth=0.5)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=6, color='white')
    
    # ===== DATABASE LAYER =====
    db_y = 2.5
    ax.text(8, db_y + 0.3, 'Database Layer', 
            ha='center', fontsize=12, fontweight='bold')
    
    # MySQL Database
    box = FancyBboxPatch((7, db_y-0.3), 2, 0.6, 
                        boxstyle="round,pad=0.05", 
                        facecolor=colors['database'], 
                        alpha=0.8, edgecolor='black', linewidth=1)
    ax.add_patch(box)
    ax.text(8, db_y, 'MySQL Database\n(autoguardian_fuel_db)', 
            ha='center', va='center', fontsize=10, color='white', fontweight='bold')
    
    # ===== EXTERNAL SERVICES =====
    ext_y = 1
    ax.text(13, ext_y + 0.3, 'External Services', 
            ha='center', fontsize=12, fontweight='bold')
    
    external_services = [
        ('Google Gemini API', 11.5, ext_y),
        ('Fuel Price APIs', 13, ext_y),
        ('Vehicle Data APIs', 14.5, ext_y),
    ]
    
    for name, x, y in external_services:
        box = FancyBboxPatch((x-0.45, y-0.15), 0.9, 0.3, 
                            boxstyle="round,pad=0.02", 
                            facecolor=colors['external'], 
                            alpha=0.7, edgecolor='black', linewidth=0.5)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=6, color='white')
    
    # ===== CONNECTIONS =====
    # Frontend to Backend connections
    for i in range(len(frontend_components)):
        x1 = frontend_components[i][1]
        y1 = frontend_components[i][2] - 0.2
        y2 = backend_y + 0.35
        
        if i < len(api_routes):
            x2 = api_routes[i][1]
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                       arrowprops=dict(arrowstyle='->', color='black', alpha=0.5, lw=0.8))
    
    # Backend to AI Services connections
    ai_connection_y = backend_y - 0.15
    ai_target_y = ai_y + 0.2
    for i in range(3):  # Business services to AI
        x1 = business_services[i][1]
        x2 = ai_services[i+1][1]  # Skip GenAI service box
        ax.annotate('', xy=(x2, ai_target_y), xytext=(x1, ai_connection_y),
                   arrowprops=dict(arrowstyle='->', color='purple', alpha=0.6, lw=1))
    
    # Backend to Database connections
    for i in range(len(api_routes)):
        x1 = api_routes[i][1]
        y1 = backend_y - 0.15
        x2 = db_models[i][1]
        y2 = data_y + 0.15
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='<->', color='orange', alpha=0.6, lw=1))
    
    # Database models to MySQL
    for model in db_models:
        x1 = model[1]
        y1 = data_y - 0.15
        x2 = 8
        y2 = db_y + 0.3
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', color='orange', alpha=0.4, lw=0.5))
    
    # AI to External Services connections
    ax.annotate('', xy=(11.5, ext_y + 0.15), xytext=(2, ai_y - 0.2),
               arrowprops=dict(arrowstyle='->', color='red', alpha=0.6, lw=1.5))
    
    # Add legend
    legend_elements = [
        patches.Rectangle((0, 0), 1, 1, facecolor=colors['frontend'], alpha=0.7, label='Frontend (React)'),
        patches.Rectangle((0, 0), 1, 1, facecolor=colors['backend'], alpha=0.7, label='Backend API (Flask)'),
        patches.Rectangle((0, 0), 1, 1, facecolor=colors['service'], alpha=0.7, label='Business Services'),
        patches.Rectangle((0, 0), 1, 1, facecolor=colors['ai'], alpha=0.7, label='AI Services'),
        patches.Rectangle((0, 0), 1, 1, facecolor=colors['database'], alpha=0.7, label='Data Layer'),
        patches.Rectangle((0, 0), 1, 1, facecolor=colors['external'], alpha=0.7, label='External APIs'),
    ]
    
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98), fontsize=8)
    
    # Add data flow indicators
    ax.text(0.2, 0.5, 'Data Flow:', fontsize=10, fontweight='bold')
    ax.text(0.2, 0.3, '→ API Requests', fontsize=8)
    ax.text(0.2, 0.1, '↔ Database Operations', fontsize=8)
    
    plt.tight_layout()
    return fig

def create_detailed_component_diagram():
    """Create detailed component interaction diagram"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'AutoGuardian - Component Interaction Diagram', 
            ha='center', va='center', fontsize=18, fontweight='bold')
    
    # Define component positions and connections
    components = {
        # Frontend Components
        'user': (1, 8, 'User Interface'),
        'react_app': (3, 8, 'React App'),
        'auth_service': (5, 8, 'Auth Service'),
        
        # Backend API
        'api_gateway': (7, 7, 'API Gateway\n(Flask Routes)'),
        'auth_middleware': (9, 7, 'JWT Auth'),
        
        # Business Logic
        'vehicle_service': (3, 5.5, 'Vehicle\nManagement'),
        'fuel_service': (5, 5.5, 'Fuel Record\nService'),
        'negotiation_bot': (7, 5.5, 'Negotiation\nBot Service'),
        'analytics_service': (9, 5.5, 'Analytics\nEngine'),
        
        # AI Layer
        'genai_service': (11, 5.5, 'GenAI Service\n(Gemini 2.0)'),
        
        # Data Layer
        'user_model': (2, 3.5, 'User\nModel'),
        'vehicle_model': (4, 3.5, 'Vehicle\nModel'),
        'fuel_model': (6, 3.5, 'Fuel Record\nModel'),
        'sale_model': (8, 3.5, 'Vehicle Sale\nModel'),
        'negotiation_model': (10, 3.5, 'Negotiation\nModel'),
        
        # Database
        'mysql_db': (6, 2, 'MySQL Database\n(autoguardian_fuel_db)'),
        
        # External Services
        'gemini_api': (12, 3.5, 'Google\nGemini API'),
    }
    
    # Color scheme
    colors = {
        'frontend': '#3B82F6',
        'backend': '#10B981',
        'ai': '#8B5CF6',
        'data': '#F59E0B',
        'external': '#EF4444',
        'database': '#92400E'
    }
    
    # Component colors mapping
    component_colors = {
        'user': colors['frontend'],
        'react_app': colors['frontend'],
        'auth_service': colors['frontend'],
        'api_gateway': colors['backend'],
        'auth_middleware': colors['backend'],
        'vehicle_service': colors['backend'],
        'fuel_service': colors['backend'],
        'negotiation_bot': colors['backend'],
        'analytics_service': colors['backend'],
        'genai_service': colors['ai'],
        'user_model': colors['data'],
        'vehicle_model': colors['data'],
        'fuel_model': colors['data'],
        'sale_model': colors['data'],
        'negotiation_model': colors['data'],
        'mysql_db': colors['database'],
        'gemini_api': colors['external'],
    }
    
    # Draw components
    for comp_id, (x, y, label) in components.items():
        color = component_colors.get(comp_id, '#6B7280')
        
        if comp_id == 'mysql_db':
            # Make database larger
            box = FancyBboxPatch((x-0.8, y-0.3), 1.6, 0.6, 
                                boxstyle="round,pad=0.05", 
                                facecolor=color, alpha=0.8, edgecolor='black', linewidth=1)
        elif comp_id == 'api_gateway':
            # Make API gateway larger
            box = FancyBboxPatch((x-0.6, y-0.3), 1.2, 0.6, 
                                boxstyle="round,pad=0.05", 
                                facecolor=color, alpha=0.8, edgecolor='black', linewidth=1)
        else:
            # Standard component size
            box = FancyBboxPatch((x-0.5, y-0.25), 1, 0.5, 
                                boxstyle="round,pad=0.03", 
                                facecolor=color, alpha=0.7, edgecolor='black', linewidth=0.5)
        
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', 
                fontsize=7, color='white', fontweight='bold')
    
    # Define connections with labels
    connections = [
        # Frontend connections
        ('user', 'react_app', 'User Actions'),
        ('react_app', 'auth_service', 'Login/Register'),
        ('react_app', 'api_gateway', 'HTTP Requests'),
        
        # Backend connections
        ('api_gateway', 'auth_middleware', 'Auth Check'),
        ('api_gateway', 'vehicle_service', 'Vehicle APIs'),
        ('api_gateway', 'fuel_service', 'Fuel APIs'),
        ('api_gateway', 'negotiation_bot', 'Negotiate APIs'),
        ('api_gateway', 'analytics_service', 'Analytics APIs'),
        
        # AI connections
        ('negotiation_bot', 'genai_service', 'AI Requests'),
        ('genai_service', 'gemini_api', 'API Calls'),
        
        # Data connections
        ('vehicle_service', 'vehicle_model', 'CRUD Ops'),
        ('fuel_service', 'fuel_model', 'CRUD Ops'),
        ('negotiation_bot', 'sale_model', 'Sale Ops'),
        ('negotiation_bot', 'negotiation_model', 'Chat Ops'),
        ('auth_service', 'user_model', 'User Ops'),
        
        # Database connections
        ('user_model', 'mysql_db', 'SQL'),
        ('vehicle_model', 'mysql_db', 'SQL'),
        ('fuel_model', 'mysql_db', 'SQL'),
        ('sale_model', 'mysql_db', 'SQL'),
        ('negotiation_model', 'mysql_db', 'SQL'),
    ]
    
    # Draw connections
    for start_comp, end_comp, label in connections:
        if start_comp in components and end_comp in components:
            x1, y1, _ = components[start_comp]
            x2, y2, _ = components[end_comp]
            
            # Calculate arrow positions
            dx = x2 - x1
            dy = y2 - y1
            
            # Offset from component edges
            offset = 0.3
            if abs(dx) > abs(dy):  # Horizontal connection
                x1_adj = x1 + (offset if dx > 0 else -offset)
                y1_adj = y1
                x2_adj = x2 + (-offset if dx > 0 else offset)
                y2_adj = y2
            else:  # Vertical connection
                x1_adj = x1
                y1_adj = y1 + (offset if dy > 0 else -offset)
                x2_adj = x2
                y2_adj = y2 + (-offset if dy > 0 else offset)
            
            # Draw arrow
            ax.annotate('', xy=(x2_adj, y2_adj), xytext=(x1_adj, y1_adj),
                       arrowprops=dict(arrowstyle='->', color='black', alpha=0.6, lw=0.8))
            
            # Add label at midpoint
            mid_x = (x1_adj + x2_adj) / 2
            mid_y = (y1_adj + y2_adj) / 2
            ax.text(mid_x, mid_y, label, ha='center', va='center', 
                    fontsize=6, bbox=dict(boxstyle="round,pad=0.2", 
                                         facecolor='white', alpha=0.8, edgecolor='none'))
    
    # Add layer labels
    ax.text(0.5, 8.5, 'Presentation Layer', ha='left', va='center', 
            fontsize=10, fontweight='bold', rotation=90)
    ax.text(0.5, 6.5, 'Application Layer', ha='left', va='center', 
            fontsize=10, fontweight='bold', rotation=90)
    ax.text(0.5, 4.5, 'Business Logic', ha='left', va='center', 
            fontsize=10, fontweight='bold', rotation=90)
    ax.text(0.5, 2.5, 'Data Access Layer', ha='left', va='center', 
            fontsize=10, fontweight='bold', rotation=90)
    
    plt.tight_layout()
    return fig

def main():
    """Generate both architecture diagrams"""
    print("Generating AutoGuardian System Architecture Diagrams...")
    
    # Generate main architecture diagram
    print("Creating main architecture diagram...")
    fig1 = create_architecture_diagram()
    output_path1 = "C:\\Users\\chan-shinan\\Documents\\icbt\\final project\\shinan_final_project\\autoguardian-fuel-system\\AutoGuardian_System_Architecture.png"
    fig1.savefig(output_path1, dpi=300, bbox_inches='tight', 
                 facecolor='white', edgecolor='none')
    print(f"Main architecture diagram saved to: {output_path1}")
    
    # Generate detailed component diagram
    print("Creating detailed component diagram...")
    fig2 = create_detailed_component_diagram()
    output_path2 = "C:\\Users\\chan-shinan\\Documents\\icbt\\final project\\shinan_final_project\\autoguardian-fuel-system\\AutoGuardian_Component_Diagram.png"
    fig2.savefig(output_path2, dpi=300, bbox_inches='tight', 
                 facecolor='white', edgecolor='none')
    print(f"Component diagram saved to: {output_path2}")
    
    print("Architecture diagrams generated successfully!")
    
    # Show diagrams
    plt.show()

if __name__ == "__main__":
    main()