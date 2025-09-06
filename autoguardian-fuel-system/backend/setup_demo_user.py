#!/usr/bin/env python3
"""
Setup Demo User for AutoGuardian System
"""

from app import create_app, db
from models.user import User, UserPreferences
from werkzeug.security import generate_password_hash

def setup_demo_user():
    """Create demo user if it doesn't exist"""
    
    app = create_app()
    
    with app.app_context():
        try:
            # Check if demo user already exists
            existing_user = User.query.filter(
                (User.username == 'testuser') | 
                (User.email == 'testuser@autoguardian.com')
            ).first()
            
            if existing_user:
                print("Demo user already exists!")
                print(f"Username: {existing_user.username}")
                print(f"Email: {existing_user.email}")
                return
            
            # Create demo user
            demo_user = User(
                username='testuser',
                email='testuser@autoguardian.com',
                password_hash=generate_password_hash('TestPassword123!'),
                first_name='Demo',
                last_name='User',
                phone='+1234567890',
                is_active=True
            )
            
            db.session.add(demo_user)
            db.session.flush()  # Flush to get the user ID
            
            # Create user preferences
            preferences = UserPreferences(
                user_id=demo_user.id,
                preferred_units='metric',
                currency='USD',
                timezone='UTC',
                notifications_enabled=True
            )
            
            db.session.add(preferences)
            db.session.commit()
            
            print("✅ Demo user created successfully!")
            print(f"Username: {demo_user.username}")
            print(f"Email: {demo_user.email}")
            print("Password: TestPassword123!")
            print(f"User ID: {demo_user.id}")
            
        except Exception as e:
            print(f"❌ Error creating demo user: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    setup_demo_user()