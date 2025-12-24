"""
SmartLogX - Users Master Table Setup Script
Run this script to create the users_master table and add sample users.

Usage:
    python setup_users_master.py

Make sure Django settings are configured before running.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartlogx.settings')
django.setup()

from django.db import connection
from django.contrib.auth.hashers import make_password


def create_users_master_table():
    """Create the users_master table if it doesn't exist"""
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users_master (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                EMP_ID VARCHAR(255) NOT NULL UNIQUE,
                EMP_NAME VARCHAR(255) NOT NULL,
                MOBILE_NUMBER VARCHAR(20),
                EMAIL VARCHAR(255) NOT NULL UNIQUE,
                ROLE VARCHAR(100) NOT NULL,
                ROLL VARCHAR(255),
                PASSWORD VARCHAR(255) NOT NULL,
                IS_FIRST_LOGIN BOOLEAN DEFAULT 1,
                CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
                UPDATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_emp_id (EMP_ID),
                INDEX idx_email (EMAIL),
                INDEX idx_role (ROLE)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ users_master table created/verified")


def create_sample_users():
    """Create sample users with properly hashed passwords"""
    
    # Default password for all sample users
    default_password = make_password('Temp@123')
    
    sample_users = [
        {
            'emp_id': 'EMP001',
            'emp_name': 'John Developer',
            'mobile': '9876543210',
            'email': 'john.dev@smartlogx.com',
            'role': 'SOFTWARE DEVELOPER',
            'roll': 'Backend Team'
        },
        {
            'emp_id': 'EMP002',
            'emp_name': 'Jane Tester',
            'mobile': '9876543211',
            'email': 'jane.test@smartlogx.com',
            'role': 'SOFTWARE TESTER',
            'roll': 'QA Team'
        },
        {
            'emp_id': 'EMP003',
            'emp_name': 'Mike Designer',
            'mobile': '9876543212',
            'email': 'mike.design@smartlogx.com',
            'role': 'UI UX DESIGNER',
            'roll': 'Design Team'
        },
        {
            'emp_id': 'EMP004',
            'emp_name': 'Sarah Coordinator',
            'mobile': '9876543213',
            'email': 'sarah.coord@smartlogx.com',
            'role': 'IT COORDINATOR',
            'roll': 'IT Operations'
        }
    ]
    
    with connection.cursor() as cursor:
        for user in sample_users:
            try:
                cursor.execute("""
                    INSERT INTO users_master 
                    (EMP_ID, EMP_NAME, MOBILE_NUMBER, EMAIL, ROLE, ROLL, PASSWORD, IS_FIRST_LOGIN)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, 1)
                """, [
                    user['emp_id'],
                    user['emp_name'],
                    user['mobile'],
                    user['email'],
                    user['role'],
                    user['roll'],
                    default_password
                ])
                print(f"✓ Created user: {user['emp_name']} ({user['emp_id']})")
            except Exception as e:
                if 'Duplicate entry' in str(e):
                    print(f"⚠ User already exists: {user['emp_name']} ({user['emp_id']})")
                else:
                    print(f"✗ Error creating {user['emp_name']}: {e}")


def show_all_users():
    """Display all users in the table"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ID, EMP_ID, EMP_NAME, EMAIL, ROLE, IS_FIRST_LOGIN, CREATED_AT
            FROM users_master
            ORDER BY CREATED_AT DESC
        """)
        rows = cursor.fetchall()
        
        if rows:
            print("\n" + "="*80)
            print("USERS IN DATABASE")
            print("="*80)
            print(f"{'ID':<5} {'EMP_ID':<10} {'NAME':<20} {'EMAIL':<30} {'ROLE':<20}")
            print("-"*80)
            for row in rows:
                print(f"{row[0]:<5} {row[1]:<10} {row[2]:<20} {row[3]:<30} {row[4]:<20}")
            print("="*80)
            print(f"Total users: {len(rows)}")
        else:
            print("\nNo users found in database.")


def main():
    print("\n" + "="*50)
    print("SmartLogX - Users Master Setup")
    print("="*50 + "\n")
    
    try:
        # Create table
        create_users_master_table()
        
        # Create sample users
        print("\nCreating sample users (password: Temp@123)...")
        create_sample_users()
        
        # Show all users
        show_all_users()
        
        print("\n✓ Setup complete!")
        print("\nSample users can login with:")
        print("  - Username: EMP_ID (e.g., EMP001) or Email")
        print("  - Password: Temp@123")
        print("  - They will be prompted to change password on first login.\n")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
