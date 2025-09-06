#!/usr/bin/env python3
"""
Update demo user password to a known value
"""

from app import create_app, db
from models.user import User
from werkzeug.security import generate_password_hash
import bcrypt

def update_demo_password():
    """Update demo user password"""
    
    app = create_app()
    
    with app.app_context():
        try:
            # Find the demo user
            user = User.query.filter_by(username='testuser').first()
            
            if user:
                print(f"Found user: {user.username} ({user.email})")
                
                # Update password to 'secret123'
                new_password = 'secret123'
                
                # Use bcrypt directly to be compatible
                hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                user.password_hash = hashed.decode('utf-8')
                
                db.session.commit()
                print(f"Password updated successfully!")
                print(f"New hash: {user.password_hash}")
                
                # Test the new password
                if bcrypt.checkpw(new_password.encode('utf-8'), user.password_hash.encode('utf-8')):
                    print("Password verification: SUCCESS!")
                else:
                    print("Password verification: FAILED!")
                    
            else:
                print("Demo user not found")
                
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    update_demo_password()