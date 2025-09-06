#!/usr/bin/env python3
"""
AutoGuardian Fuel Management System - ER Diagram Generator
This script generates comprehensive Entity-Relationship diagrams for the database schema.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Polygon, Circle, Rectangle
import numpy as np

def create_comprehensive_er_diagram():
    """Generate comprehensive ER diagram with all entities and relationships"""
    
    fig, ax = plt.subplots(1, 1, figsize=(20, 14))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # Set background
    ax.add_patch(Rectangle((0, 0), 20, 14, facecolor='#F8FAFC', alpha=0.5))
    
    # Title
    ax.text(10, 13.5, 'AutoGuardian Database - Entity Relationship Diagram', 
            ha='center', va='center', fontsize=18, fontweight='bold', color='#1F2937')
    ax.text(10, 13.1, 'Complete Database Schema with Relationships and Constraints', 
            ha='center', va='center', fontsize=12, style='italic', color='#6B7280')
    
    # Define colors
    colors = {
        'entity': '#3B82F6',        # Blue for entities
        'attribute': '#10B981',     # Green for attributes  
        'key_attr': '#F59E0B',      # Orange for key attributes
        'relationship': '#EF4444',  # Red for relationships
        'weak_entity': '#8B5CF6',   # Purple for weak entities
        'derived_attr': '#6B7280'   # Gray for derived attributes
    }
    
    # Define entities with their positions and attributes
    entities = {
        'users': {
            'pos': (3, 11),
            'size': (2.5, 1.8),
            'attributes': {
                'id': {'type': 'key', 'pos': (1.5, 12)},
                'username': {'type': 'normal', 'pos': (2.2, 12.3)},
                'email': {'type': 'normal', 'pos': (3.8, 12.3)},
                'first_name': {'type': 'normal', 'pos': (4.5, 12)},
                'last_name': {'type': 'normal', 'pos': (4.2, 11.5)},
                'phone': {'type': 'normal', 'pos': (3.8, 10.7)},
                'password_hash': {'type': 'normal', 'pos': (2.2, 10.7)},
                'is_active': {'type': 'normal', 'pos': (1.5, 11)},
                'created_at': {'type': 'normal', 'pos': (1.8, 11.5)},
                'updated_at': {'type': 'normal', 'pos': (1.2, 11.8)}
            }
        },
        
        'vehicles': {
            'pos': (8, 11),
            'size': (3, 2.2),
            'attributes': {
                'id': {'type': 'key', 'pos': (6.5, 12.5)},
                'vehicle_name': {'type': 'normal', 'pos': (7.2, 12.8)},
                'make': {'type': 'normal', 'pos': (8.8, 12.8)},
                'model': {'type': 'normal', 'pos': (9.5, 12.5)},
                'year': {'type': 'normal', 'pos': (9.8, 12)},
                'vehicle_class': {'type': 'normal', 'pos': (9.5, 11.5)},
                'engine_size': {'type': 'normal', 'pos': (8.8, 10.2)},
                'cylinders': {'type': 'normal', 'pos': (8, 10)},
                'transmission': {'type': 'normal', 'pos': (7.2, 10.2)},
                'fuel_type': {'type': 'normal', 'pos': (6.5, 10.5)},
                'tank_capacity': {'type': 'normal', 'pos': (6.2, 11)},
                'is_active': {'type': 'normal', 'pos': (6.5, 11.5)},
                'created_at': {'type': 'normal', 'pos': (10.2, 10.8)}
            }
        },
        
        'fuel_records': {
            'pos': (14, 11),
            'size': (3.5, 2.5),
            'attributes': {
                'id': {'type': 'key', 'pos': (12.5, 12.8)},
                'record_date': {'type': 'normal', 'pos': (13.2, 13.2)},
                'record_time': {'type': 'normal', 'pos': (14.8, 13.2)},
                'existing_tank_%': {'type': 'normal', 'pos': (15.5, 12.8)},
                'after_refuel_%': {'type': 'normal', 'pos': (16, 12.3)},
                'odometer_value': {'type': 'normal', 'pos': (15.8, 11.8)},
                'driving_type': {'type': 'normal', 'pos': (15.5, 11.2)},
                'location': {'type': 'normal', 'pos': (14.8, 10.8)},
                'fuel_price': {'type': 'normal', 'pos': (14, 10.5)},
                'calculated_fuel_added': {'type': 'derived', 'pos': (13.2, 10.8)},
                'total_cost': {'type': 'derived', 'pos': (12.5, 11.2)},
                'consumption_l_100km': {'type': 'derived', 'pos': (12, 11.8)},
                'notes': {'type': 'normal', 'pos': (12.2, 12.3)}
            }
        },
        
        'ai_recommendations': {
            'pos': (3, 7.5),
            'size': (3.2, 2.3),
            'attributes': {
                'id': {'type': 'key', 'pos': (1.5, 9)},
                'recommendation_type': {'type': 'normal', 'pos': (2.2, 9.5)},
                'title': {'type': 'normal', 'pos': (3.8, 9.5)},
                'recommendation_text': {'type': 'normal', 'pos': (4.7, 9)},
                'priority_level': {'type': 'normal', 'pos': (4.5, 8.5)},
                'category': {'type': 'normal', 'pos': (4.2, 8)},
                'impact_score': {'type': 'normal', 'pos': (3.8, 7.5)},
                'is_read': {'type': 'normal', 'pos': (3, 7.2)},
                'confidence_level': {'type': 'normal', 'pos': (2.2, 7.5)},
                'ai_model_used': {'type': 'normal', 'pos': (1.5, 8)},
                'created_at': {'type': 'normal', 'pos': (1.2, 8.5)},
                'expires_at': {'type': 'normal', 'pos': (1.8, 6.5)}
            }
        },
        
        'ml_predictions': {
            'pos': (8.5, 7.5),
            'size': (3, 2),
            'attributes': {
                'id': {'type': 'key', 'pos': (7, 8.8)},
                'combined_l_100km': {'type': 'normal', 'pos': (7.8, 9.2)},
                'highway_l_100km': {'type': 'normal', 'pos': (9.2, 9.2)},
                'city_l_100km': {'type': 'normal', 'pos': (10, 8.8)},
                'emissions_g_km': {'type': 'normal', 'pos': (10.2, 8.3)},
                'efficiency_rating': {'type': 'derived', 'pos': (10, 7.8)},
                'confidence_score': {'type': 'normal', 'pos': (9.2, 7.3)},
                'model_version': {'type': 'normal', 'pos': (8.5, 7)},
                'prediction_source': {'type': 'normal', 'pos': (7.8, 7.3)},
                'prediction_date': {'type': 'normal', 'pos': (7, 7.8)},
                'annual_fuel_cost': {'type': 'derived', 'pos': (6.8, 8.3)}
            }
        },
        
        'vehicle_sales': {
            'pos': (14, 7.5),
            'size': (2.8, 2),
            'attributes': {
                'id': {'type': 'key', 'pos': (12.5, 8.8)},
                'selling_price': {'type': 'normal', 'pos': (13.2, 9.2)},
                'minimum_price': {'type': 'normal', 'pos': (14.8, 9.2)},
                'features': {'type': 'normal', 'pos': (15.5, 8.8)},
                'description': {'type': 'normal', 'pos': (15.3, 8.3)},
                'is_active': {'type': 'normal', 'pos': (14.8, 7.8)},
                'is_sold': {'type': 'normal', 'pos': (14, 7.3)},
                'created_at': {'type': 'normal', 'pos': (13.2, 7.8)},
                'updated_at': {'type': 'normal', 'pos': (12.5, 8.3)}
            }
        },
        
        'negotiations': {
            'pos': (18, 7.5),
            'size': (2.5, 2),
            'attributes': {
                'id': {'type': 'key', 'pos': (16.8, 8.8)},
                'buyer_name': {'type': 'normal', 'pos': (17.5, 9.2)},
                'buyer_email': {'type': 'normal', 'pos': (18.7, 9.2)},
                'buyer_contact': {'type': 'normal', 'pos': (19.2, 8.8)},
                'final_offer': {'type': 'normal', 'pos': (19, 8.3)},
                'chat_history': {'type': 'normal', 'pos': (18.7, 7.8)},
                'status': {'type': 'normal', 'pos': (18, 7.3)},
                'created_at': {'type': 'normal', 'pos': (17.5, 7.8)},
                'updated_at': {'type': 'normal', 'pos': (16.8, 8.3)}
            }
        },
        
        'user_preferences': {
            'pos': (3, 4),
            'size': (2.5, 1.5),
            'attributes': {
                'id': {'type': 'key', 'pos': (1.8, 5)},
                'currency': {'type': 'normal', 'pos': (2.5, 5.3)},
                'distance_unit': {'type': 'normal', 'pos': (3.7, 5.3)},
                'volume_unit': {'type': 'normal', 'pos': (4.2, 5)},
                'date_format': {'type': 'normal', 'pos': (4, 4.5)},
                'notification_email': {'type': 'normal', 'pos': (3.7, 4)},
                'created_at': {'type': 'normal', 'pos': (2.5, 3.7)},
                'updated_at': {'type': 'normal', 'pos': (1.8, 4)}
            }
        },
        
        'vehicle_statistics': {
            'pos': (8.5, 4),
            'size': (3, 1.8),
            'attributes': {
                'id': {'type': 'key', 'pos': (7, 5.2)},
                'total_fuel_consumed': {'type': 'derived', 'pos': (7.8, 5.5)},
                'total_distance': {'type': 'derived', 'pos': (9.2, 5.5)},
                'total_cost': {'type': 'derived', 'pos': (10, 5.2)},
                'avg_consumption': {'type': 'derived', 'pos': (10.2, 4.7)},
                'total_refuels': {'type': 'derived', 'pos': (9.5, 4.2)},
                'efficiency_trend': {'type': 'derived', 'pos': (8.5, 3.8)},
                'last_updated': {'type': 'normal', 'pos': (7.5, 4.2)},
                'last_fuel_date': {'type': 'normal', 'pos': (7, 4.7)}
            }
        }
    }
    
    # Draw entities
    for entity_name, entity_data in entities.items():
        draw_entity(ax, entity_name, entity_data, colors)
    
    # Define relationships
    relationships = [
        {
            'name': 'owns',
            'from_entity': 'users',
            'to_entity': 'vehicles',
            'from_pos': (5.5, 11),
            'to_pos': (6.5, 11),
            'cardinality': ('1', 'M'),
            'type': 'identifying'
        },
        {
            'name': 'has_records',
            'from_entity': 'vehicles', 
            'to_entity': 'fuel_records',
            'from_pos': (11, 11),
            'to_pos': (12.5, 11),
            'cardinality': ('1', 'M'),
            'type': 'identifying'
        },
        {
            'name': 'receives',
            'from_entity': 'users',
            'to_entity': 'ai_recommendations', 
            'from_pos': (3, 9.2),
            'to_pos': (3, 9.8),
            'cardinality': ('1', 'M'),
            'type': 'non-identifying'
        },
        {
            'name': 'generates_for',
            'from_entity': 'vehicles',
            'to_entity': 'ai_recommendations',
            'from_pos': (6.5, 9.8),
            'to_pos': (4.7, 8.5),
            'cardinality': ('1', 'M'),
            'type': 'non-identifying'
        },
        {
            'name': 'predicts',
            'from_entity': 'vehicles',
            'to_entity': 'ml_predictions',
            'from_pos': (8, 8.8),
            'to_pos': (8.5, 8.5),
            'cardinality': ('1', 'M'),
            'type': 'non-identifying'
        },
        {
            'name': 'sells',
            'from_entity': 'users',
            'to_entity': 'vehicle_sales',
            'from_pos': (5.5, 9),
            'to_pos': (12.2, 8.5),
            'cardinality': ('1', 'M'),
            'type': 'non-identifying'
        },
        {
            'name': 'lists',
            'from_entity': 'vehicles',
            'to_entity': 'vehicle_sales',
            'from_pos': (11, 9.5),
            'to_pos': (12.2, 8),
            'cardinality': ('1', '1'),
            'type': 'non-identifying'
        },
        {
            'name': 'negotiates',
            'from_entity': 'vehicle_sales',
            'to_entity': 'negotiations',
            'from_pos': (16.8, 7.5),
            'to_pos': (17.2, 7.5),
            'cardinality': ('1', 'M'),
            'type': 'identifying'
        },
        {
            'name': 'has_preferences',
            'from_entity': 'users',
            'to_entity': 'user_preferences',
            'from_pos': (3, 9.2),
            'to_pos': (3, 5.5),
            'cardinality': ('1', '1'),
            'type': 'identifying'
        },
        {
            'name': 'has_statistics',
            'from_entity': 'vehicles',
            'to_entity': 'vehicle_statistics',
            'from_pos': (8.5, 8.8),
            'to_pos': (8.5, 5.8),
            'cardinality': ('1', '1'),
            'type': 'identifying'
        }
    ]
    
    # Draw relationships
    for rel in relationships:
        draw_relationship(ax, rel, colors)
    
    # Add legend
    legend_x = 1
    legend_y = 2.5
    ax.text(legend_x, legend_y + 0.5, 'ER Diagram Legend:', fontsize=12, fontweight='bold')
    
    # Entity legend
    draw_entity_box(ax, legend_x, legend_y, 0.8, 0.3, colors['entity'])
    ax.text(legend_x + 1, legend_y + 0.15, 'Entity', fontsize=10, va='center')
    
    # Key attribute legend
    draw_attribute_circle(ax, legend_x, legend_y - 0.4, 0.08, colors['key_attr'])
    ax.text(legend_x + 0.3, legend_y - 0.4, 'Key Attribute', fontsize=10, va='center')
    
    # Normal attribute legend
    draw_attribute_circle(ax, legend_x, legend_y - 0.7, 0.08, colors['attribute'])
    ax.text(legend_x + 0.3, legend_y - 0.7, 'Normal Attribute', fontsize=10, va='center')
    
    # Derived attribute legend
    draw_derived_attribute(ax, legend_x, legend_y - 1.0, 0.08, colors['derived_attr'])
    ax.text(legend_x + 0.3, legend_y - 1.0, 'Derived Attribute', fontsize=10, va='center')
    
    # Relationship legend
    draw_diamond(ax, legend_x + 0.15, legend_y - 1.3, 0.3, 0.15, colors['relationship'])
    ax.text(legend_x + 0.6, legend_y - 1.3, 'Relationship', fontsize=10, va='center')
    
    # Cardinality legend
    ax.text(legend_x + 3, legend_y + 0.2, 'Cardinalities:', fontsize=11, fontweight='bold')
    ax.text(legend_x + 3, legend_y - 0.1, '1 = One', fontsize=10)
    ax.text(legend_x + 3, legend_y - 0.4, 'M = Many', fontsize=10)
    ax.text(legend_x + 3, legend_y - 0.7, '── = Identifying Relationship', fontsize=10)
    ax.text(legend_x + 3, legend_y - 1.0, '- - = Non-identifying Relationship', fontsize=10)
    
    plt.tight_layout()
    return fig

def draw_entity(ax, name, entity_data, colors):
    """Draw an entity with its attributes"""
    pos = entity_data['pos']
    size = entity_data['size']
    attributes = entity_data['attributes']
    
    # Draw entity rectangle
    draw_entity_box(ax, pos[0] - size[0]/2, pos[1] - size[1]/2, size[0], size[1], colors['entity'])
    
    # Entity name
    ax.text(pos[0], pos[1], name.upper(), ha='center', va='center', 
            fontsize=11, fontweight='bold', color='white')
    
    # Draw attributes
    for attr_name, attr_data in attributes.items():
        attr_pos = attr_data['pos']
        attr_type = attr_data['type']
        
        if attr_type == 'key':
            draw_attribute_circle(ax, attr_pos[0], attr_pos[1], 0.12, colors['key_attr'])
            # Underline key attributes
            ax.text(attr_pos[0], attr_pos[1] - 0.35, attr_name, ha='center', va='center',
                   fontsize=8, fontweight='bold', style='italic')
            ax.plot([attr_pos[0] - 0.2, attr_pos[0] + 0.2], [attr_pos[1] - 0.45, attr_pos[1] - 0.45], 
                   color='black', linewidth=1)
        elif attr_type == 'derived':
            draw_derived_attribute(ax, attr_pos[0], attr_pos[1], 0.12, colors['derived_attr'])
            ax.text(attr_pos[0], attr_pos[1] - 0.35, attr_name, ha='center', va='center',
                   fontsize=8, style='italic')
        else:
            draw_attribute_circle(ax, attr_pos[0], attr_pos[1], 0.12, colors['attribute'])
            ax.text(attr_pos[0], attr_pos[1] - 0.35, attr_name, ha='center', va='center',
                   fontsize=8)
        
        # Connect attribute to entity
        ax.plot([attr_pos[0], pos[0]], [attr_pos[1], pos[1]], 
               color='black', linewidth=0.8, alpha=0.6)

def draw_entity_box(ax, x, y, width, height, color):
    """Draw entity box"""
    box = FancyBboxPatch((x, y), width, height,
                        boxstyle="round,pad=0.02", 
                        facecolor=color, alpha=0.9, 
                        edgecolor='black', linewidth=1.5)
    ax.add_patch(box)

def draw_attribute_circle(ax, x, y, radius, color):
    """Draw attribute circle"""
    circle = Circle((x, y), radius, facecolor=color, alpha=0.8, 
                   edgecolor='black', linewidth=1)
    ax.add_patch(circle)

def draw_derived_attribute(ax, x, y, radius, color):
    """Draw derived attribute (dashed circle)"""
    circle = Circle((x, y), radius, facecolor=color, alpha=0.6, 
                   edgecolor='black', linewidth=1, linestyle='dashed')
    ax.add_patch(circle)

def draw_diamond(ax, x, y, width, height, color):
    """Draw relationship diamond"""
    diamond_points = np.array([
        [x, y + height],      # top
        [x + width, y],       # right  
        [x, y - height],      # bottom
        [x - width, y]        # left
    ])
    diamond = Polygon(diamond_points, facecolor=color, alpha=0.8, 
                     edgecolor='black', linewidth=1.2)
    ax.add_patch(diamond)

def draw_relationship(ax, rel, colors):
    """Draw relationship between entities"""
    from_pos = rel['from_pos']
    to_pos = rel['to_pos']
    name = rel['name']
    cardinality = rel['cardinality']
    rel_type = rel['type']
    
    # Calculate midpoint for relationship diamond
    mid_x = (from_pos[0] + to_pos[0]) / 2
    mid_y = (from_pos[1] + to_pos[1]) / 2
    
    # Draw relationship diamond
    draw_diamond(ax, mid_x, mid_y, 0.4, 0.2, colors['relationship'])
    ax.text(mid_x, mid_y, name, ha='center', va='center', 
            fontsize=8, color='white', fontweight='bold')
    
    # Draw lines
    if rel_type == 'identifying':
        # Solid line for identifying relationship
        line_style = '-'
        line_width = 2
    else:
        # Dashed line for non-identifying relationship  
        line_style = '--'
        line_width = 1.5
    
    ax.plot([from_pos[0], mid_x - 0.4], [from_pos[1], mid_y], 
           linestyle=line_style, color='black', linewidth=line_width)
    ax.plot([mid_x + 0.4, to_pos[0]], [mid_y, to_pos[1]], 
           linestyle=line_style, color='black', linewidth=line_width)
    
    # Add cardinality labels
    from_card_x = from_pos[0] + (mid_x - from_pos[0]) * 0.3
    from_card_y = from_pos[1] + (mid_y - from_pos[1]) * 0.3
    ax.text(from_card_x, from_card_y + 0.1, cardinality[0], ha='center', va='center',
           fontsize=10, fontweight='bold', 
           bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.8))
    
    to_card_x = to_pos[0] + (mid_x - to_pos[0]) * 0.3  
    to_card_y = to_pos[1] + (mid_y - to_pos[1]) * 0.3
    ax.text(to_card_x, to_card_y + 0.1, cardinality[1], ha='center', va='center',
           fontsize=10, fontweight='bold',
           bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.8))

def create_simplified_er_diagram():
    """Create a simplified ER diagram focusing on core entities"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Set background
    ax.add_patch(Rectangle((0, 0), 16, 10, facecolor='#F9FAFB', alpha=0.5))
    
    # Title
    ax.text(8, 9.5, 'AutoGuardian Database - Simplified ER Diagram', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    ax.text(8, 9.1, 'Core Entities and Primary Relationships', 
            ha='center', va='center', fontsize=12, style='italic')
    
    # Define core entities
    core_entities = {
        'USER': {
            'pos': (3, 7),
            'size': (2.5, 1.5),
            'key_attrs': ['id', 'username', 'email'],
            'attrs': ['first_name', 'last_name', 'phone', 'created_at']
        },
        'VEHICLE': {
            'pos': (8, 7),
            'size': (3, 1.8),
            'key_attrs': ['id'],
            'attrs': ['vehicle_name', 'make', 'model', 'year', 'fuel_type', 'tank_capacity']
        },
        'FUEL_RECORD': {
            'pos': (13, 7),
            'size': (2.8, 1.8),
            'key_attrs': ['id'],
            'attrs': ['record_date', 'odometer_value', 'fuel_price', 'total_cost']
        },
        'AI_RECOMMENDATION': {
            'pos': (3, 4),
            'size': (3, 1.5),
            'key_attrs': ['id'],
            'attrs': ['title', 'recommendation_text', 'priority_level', 'is_read']
        },
        'VEHICLE_SALE': {
            'pos': (8, 4),
            'size': (2.8, 1.5),
            'key_attrs': ['id'],
            'attrs': ['selling_price', 'description', 'is_active', 'is_sold']
        },
        'NEGOTIATION': {
            'pos': (13, 4),
            'size': (2.5, 1.5),
            'key_attrs': ['id'],
            'attrs': ['buyer_name', 'final_offer', 'status', 'created_at']
        }
    }
    
    # Colors
    entity_color = '#2563EB'
    key_color = '#DC2626'
    attr_color = '#059669'
    rel_color = '#7C2D12'
    
    # Draw entities
    for name, data in core_entities.items():
        pos = data['pos']
        size = data['size']
        
        # Entity box
        box = FancyBboxPatch((pos[0] - size[0]/2, pos[1] - size[1]/2), size[0], size[1],
                            boxstyle="round,pad=0.05", 
                            facecolor=entity_color, alpha=0.9, 
                            edgecolor='black', linewidth=2)
        ax.add_patch(box)
        
        # Entity name
        ax.text(pos[0], pos[1] + 0.4, name, ha='center', va='center', 
                fontsize=11, fontweight='bold', color='white')
        
        # Key attributes (underlined)
        y_offset = 0.1
        for key_attr in data['key_attrs']:
            ax.text(pos[0], pos[1] + y_offset, key_attr, ha='center', va='center',
                   fontsize=9, fontweight='bold', color='yellow')
            ax.plot([pos[0] - 0.3, pos[0] + 0.3], 
                   [pos[1] + y_offset - 0.08, pos[1] + y_offset - 0.08], 
                   color='yellow', linewidth=1.5)
            y_offset -= 0.2
        
        # Normal attributes  
        for attr in data['attrs'][:3]:  # Show only first 3 to avoid clutter
            ax.text(pos[0], pos[1] + y_offset, attr, ha='center', va='center',
                   fontsize=8, color='white')
            y_offset -= 0.15
    
    # Define simplified relationships
    simple_relationships = [
        ('USER', 'VEHICLE', 'owns', (5.5, 7), '1', 'M'),
        ('VEHICLE', 'FUEL_RECORD', 'has', (10.5, 7), '1', 'M'), 
        ('USER', 'AI_RECOMMENDATION', 'receives', (3, 5.5), '1', 'M'),
        ('USER', 'VEHICLE_SALE', 'creates', (5.5, 5.5), '1', 'M'),
        ('VEHICLE_SALE', 'NEGOTIATION', 'negotiated_via', (10.5, 4), '1', 'M'),
    ]
    
    # Draw relationships
    for from_entity, to_entity, rel_name, rel_pos, card1, card2 in simple_relationships:
        from_pos = core_entities[from_entity]['pos']
        to_pos = core_entities[to_entity]['pos']
        
        # Relationship diamond
        draw_diamond(ax, rel_pos[0], rel_pos[1], 0.5, 0.25, rel_color)
        ax.text(rel_pos[0], rel_pos[1], rel_name, ha='center', va='center',
                fontsize=8, color='white', fontweight='bold')
        
        # Lines
        ax.plot([from_pos[0], rel_pos[0] - 0.5], [from_pos[1], rel_pos[1]], 
               color='black', linewidth=2)
        ax.plot([rel_pos[0] + 0.5, to_pos[0]], [rel_pos[1], to_pos[1]], 
               color='black', linewidth=2)
        
        # Cardinalities
        mid1_x = (from_pos[0] + rel_pos[0]) / 2
        mid1_y = (from_pos[1] + rel_pos[1]) / 2
        ax.text(mid1_x, mid1_y + 0.15, card1, ha='center', va='center',
               fontsize=10, fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.1", facecolor='white'))
        
        mid2_x = (to_pos[0] + rel_pos[0]) / 2  
        mid2_y = (to_pos[1] + rel_pos[1]) / 2
        ax.text(mid2_x, mid2_y + 0.15, card2, ha='center', va='center',
               fontsize=10, fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.1", facecolor='white'))
    
    # Add constraints info
    constraints_text = [
        "Key Constraints:",
        "• All entities have auto-increment primary keys",
        "• Foreign keys enforce referential integrity", 
        "• Unique constraints on username/email",
        "• Check constraints on enum fields",
        "",
        "Cardinality:",
        "• 1:M = One-to-Many relationship",
        "• Each user can own multiple vehicles",
        "• Each vehicle can have multiple fuel records"
    ]
    
    y_pos = 2.5
    for text in constraints_text:
        style = 'bold' if text.endswith(':') else 'normal'
        ax.text(1, y_pos, text, ha='left', va='center', fontsize=9, 
               fontweight=style, color='#374151')
        y_pos -= 0.2
    
    plt.tight_layout()
    return fig

def main():
    """Generate ER diagrams"""
    print("Generating AutoGuardian ER Diagrams...")
    
    diagrams = [
        ("Comprehensive ER Diagram", create_comprehensive_er_diagram, "AutoGuardian_Complete_ER_Diagram.png"),
        ("Simplified ER Diagram", create_simplified_er_diagram, "AutoGuardian_Simplified_ER_Diagram.png"),
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
    
    print("\n[SUCCESS] All ER diagrams generated!")
    print("\nGenerated Diagrams:")
    print("1. Complete ER Diagram - Full database schema with all entities and attributes")
    print("2. Simplified ER Diagram - Core entities with primary relationships")
    
    print("\nER Diagram Features:")
    print("- Standard ER notation with entities, attributes, and relationships")
    print("- Key attributes (underlined) and derived attributes (dashed)")
    print("- Relationship diamonds with cardinality indicators")
    print("- Identifying vs non-identifying relationships")
    print("- Entity integrity and referential integrity constraints")
    print("- Color-coded components for better readability")

if __name__ == "__main__":
    main()