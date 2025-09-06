"""
AutoGuardian Database Setup Script
Run this script to create the database and tables automatically
"""

import mysql.connector
from mysql.connector import Error
import os

def create_database():
    """Create the AutoGuardian database and tables"""
    
    # Database configuration
    config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '',  # Enter your MySQL root password here
        'port': 3306,
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_unicode_ci'
    }


    
    # Read the SQL file
    sql_file_path = os.path.join(os.path.dirname(__file__), 'migrations', 'create_database.sql')
    
    try:
        # Read the SQL script
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        
        # Split the script into individual statements
        sql_statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
        
        print("🔄 Connecting to MySQL server...")
        
        # Connect to MySQL server
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        print("✅ Connected to MySQL server successfully!")
        
        # Execute each SQL statement
        for i, statement in enumerate(sql_statements, 1):
            if statement.strip():
                try:
                    # Handle USE database statement separately
                    if statement.strip().upper().startswith('USE'):
                        cursor.execute(statement)
                        print(f"📊 Switched to autoguardian_db")
                    else:
                        cursor.execute(statement)
                        
                        # Check if it's a CREATE statement to provide feedback
                        if statement.strip().upper().startswith('CREATE DATABASE'):
                            print(f"🗄️  Created database: autoguardian_db")
                        elif statement.strip().upper().startswith('CREATE TABLE'):
                            table_name = statement.split()[5] if len(statement.split()) > 5 else "table"
                            print(f"📋 Created table: {table_name}")
                        elif statement.strip().upper().startswith('INSERT'):
                            print(f"📝 Inserted sample data")
                        elif statement.strip().upper().startswith('CREATE TRIGGER'):
                            print(f"⚙️  Created database trigger")
                
                except Error as e:
                    if "already exists" in str(e).lower():
                        print(f"⚠️  Skipping: Already exists")
                    else:
                        print(f"❌ Error executing statement {i}: {e}")
                        print(f"Statement: {statement[:100]}...")
        
        # Commit all changes
        connection.commit()
        print("\n🎉 Database setup completed successfully!")
        
        # Verify tables were created
        cursor.execute("USE autoguardian_db")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"\n📋 Created tables ({len(tables)}):")
        for table in tables:
            print(f"   • {table[0]}")
        
        # Check sample data
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"\n👥 Sample users created: {user_count}")
        
        cursor.execute("SELECT COUNT(*) FROM vehicles") 
        vehicle_count = cursor.fetchone()[0]
        print(f"🚗 Sample vehicles created: {vehicle_count}")
        
    except FileNotFoundError:
        print(f"❌ SQL file not found: {sql_file_path}")
        print("Make sure you're running this script from the backend directory")
    except Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("\n🔌 Database connection closed")

def test_connection():
    """Test database connection"""
    config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '',  # Enter your MySQL root password here
        'database': 'autoguardian_db',
        'port': 3306
    }
    
    try:
        print("🔄 Testing database connection...")
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()
            print(f"✅ Connected to database: {db_name[0]}")
            
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"📋 Available tables: {len(tables)}")
            
            return True
    except Error as e:
        print(f"❌ Connection failed: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    print("🚀 AutoGuardian Database Setup")
    print("=" * 40)
    
    # Get MySQL password from user
    import getpass
    password = getpass.getpass("Enter MySQL root password (or press Enter if no password): ")
    
    # Update the password in config
    if password:
        # You can also update the password directly in the script above
        print("⚠️  Please update the password in the script for automated setup")
    
    print("\n1. Creating database and tables...")
    create_database()
    
    print("\n2. Testing connection...")
    if test_connection():
        print("\n🎉 Database setup completed successfully!")
        print("\nYou can now run the Flask application with:")
        print("python app.py")
    else:
        print("\n❌ Database setup failed. Please check the errors above.")