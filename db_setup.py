import MySQLdb
import os
import sys
from pathlib import Path

def setup_database():
    print("========================================")
    print("  SmartLogX - Database Setup Tool")
    print("========================================")
    print("")
    
    # Get password securely
    import getpass
    try:
        password = getpass.getpass("Enter your MySQL root password: ")
    except Exception:
        password = input("Enter your MySQL root password: ")

    print("\nConnecting to MySQL...")
    
    try:
        # Connect to MySQL Server
        db = MySQLdb.connect(
            host="localhost",
            user="root",
            passwd=password
        )
        cursor = db.cursor()
        
        # Create Database
        print("Creating database 'smartlogx_db'...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS smartlogx_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print("✓ Database created successfully")
        
        # Update settings.py
        print("Updating settings.py...")
        settings_path = Path("smartlogx/settings.py")
        
        with open(settings_path, 'r') as f:
            content = f.read()
            
        # Replace password placeholder
        if 'PASSWORD": "",' in content:
            new_content = content.replace('PASSWORD": "",', f'PASSWORD": "{password}",')
        elif 'PASSWORD": "your_mysql_password",' in content:
            new_content = content.replace('PASSWORD": "your_mysql_password",', f'PASSWORD": "{password}",')
        else:
            # Regex replacement if needed, but simple replace should work for the template we created
            import re
            new_content = re.sub(r'PASSWORD": ".*",', f'PASSWORD": "{password}",', content)
            
        with open(settings_path, 'w') as f:
            f.write(new_content)
            
        print("✓ settings.py updated")
        
        # Run migrations
        print("\nRunning Django migrations...")
        os.system("python manage.py makemigrations")
        os.system("python manage.py migrate")
        
        print("\n========================================")
        print("  Database Setup Complete!")
        print("========================================")
        
    except MySQLdb.Error as e:
        print(f"\n✗ MySQL Error: {e}")
        print("Please check your password and ensure MySQL is running.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_database()
