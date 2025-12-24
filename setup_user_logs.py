"""
SmartLogX - User Logs Tables Setup Script
Run this script to create the user_logs and approval_codes tables.

Usage:
    python setup_user_logs.py

Make sure Django settings are configured before running.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartlogx.settings')
django.setup()

from django.db import connection


def create_user_logs_table():
    """Create the user_logs table"""
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_logs (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                USER_ID INT NOT NULL,
                PROJECT_TITLE VARCHAR(255) NOT NULL,
                LOG_HEADING VARCHAR(255) NOT NULL,
                LOG_DETAILS TEXT NOT NULL,
                LOG_DATE DATE NOT NULL,
                SESSION_TYPE ENUM('First Half', 'Second Half') NOT NULL,
                APPROVAL_REQUIRED BOOLEAN DEFAULT 0,
                APPROVAL_CODE VARCHAR(10) NULL,
                CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
                UPDATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_user_id (USER_ID),
                INDEX idx_log_date (LOG_DATE),
                INDEX idx_session (SESSION_TYPE),
                INDEX idx_user_date (USER_ID, LOG_DATE)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ user_logs table created/verified")


def create_approval_codes_table():
    """Create the approval_codes table"""
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS approval_codes (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                USER_ID INT NOT NULL,
                CODE VARCHAR(10) NOT NULL,
                SESSION_TYPE ENUM('First Half', 'Second Half') NOT NULL,
                CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
                EXPIRES_AT DATETIME NOT NULL,
                INDEX idx_user_code (USER_ID, CODE),
                INDEX idx_expires (EXPIRES_AT)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ approval_codes table created/verified")


def create_projects_table():
    """Create the projects table"""
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                PROJECT_NAME VARCHAR(255) NOT NULL,
                PROJECT_CODE VARCHAR(50) UNIQUE,
                DESCRIPTION TEXT,
                IS_ACTIVE BOOLEAN DEFAULT 1,
                CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_active (IS_ACTIVE),
                INDEX idx_name (PROJECT_NAME)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ projects table created/verified")


def insert_sample_projects():
    """Insert sample projects"""
    projects = [
        ('SmartLogX Development', 'SLX-DEV', 'Main SmartLogX application development'),
        ('Client Portal', 'CP-001', 'Client facing portal development'),
        ('Internal Tools', 'INT-TOOLS', 'Internal productivity tools'),
        ('Mobile App', 'MOB-APP', 'Mobile application development'),
        ('API Development', 'API-DEV', 'Backend API development'),
        ('UI/UX Design', 'UI-UX', 'User interface and experience design'),
        ('Testing & QA', 'TEST-QA', 'Quality assurance and testing'),
        ('Documentation', 'DOCS', 'Technical documentation'),
    ]
    
    with connection.cursor() as cursor:
        for name, code, desc in projects:
            try:
                cursor.execute("""
                    INSERT INTO projects (PROJECT_NAME, PROJECT_CODE, DESCRIPTION, IS_ACTIVE)
                    VALUES (%s, %s, %s, 1)
                """, [name, code, desc])
                print(f"  ✓ Added project: {name}")
            except Exception as e:
                if 'Duplicate entry' in str(e):
                    print(f"  ⚠ Project already exists: {name}")
                else:
                    print(f"  ✗ Error adding {name}: {e}")


def show_table_info():
    """Show information about created tables"""
    with connection.cursor() as cursor:
        # Count user_logs
        cursor.execute("SELECT COUNT(*) FROM user_logs")
        log_count = cursor.fetchone()[0]
        
        # Count projects
        cursor.execute("SELECT COUNT(*) FROM projects")
        project_count = cursor.fetchone()[0]
        
        print("\n" + "="*50)
        print("TABLE SUMMARY")
        print("="*50)
        print(f"user_logs: {log_count} records")
        print(f"projects: {project_count} records")
        print("approval_codes: temporary storage (auto-cleanup)")
        print("="*50)


def main():
    print("\n" + "="*50)
    print("SmartLogX - User Logs Setup")
    print("="*50 + "\n")
    
    try:
        # Create tables
        create_user_logs_table()
        create_approval_codes_table()
        create_projects_table()
        
        # Insert sample projects
        print("\nInserting sample projects...")
        insert_sample_projects()
        
        # Show summary
        show_table_info()
        
        print("\n✓ Setup complete!")
        print("\nTime Windows for Log Submission:")
        print("  - First Half:  1:00 PM - 2:30 PM IST")
        print("  - Second Half: 6:00 PM - 7:30 PM IST")
        print("\nOutside these windows, users need admin approval.\n")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
