"""
SmartLogX - Attendance Tables Setup Script
Run this script to create attendance_leave, attendance_compoff, attendance_wfh tables.

Usage:
    python setup_attendance.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartlogx.settings')
django.setup()

from django.db import connection


def create_attendance_leave_table():
    """Create the attendance_leave table"""
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance_leave (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                USER_ID INT NOT NULL,
                LEAVE_DATE DATE NOT NULL,
                LEAVE_TYPE ENUM('Planned', 'Casual', 'Emergency', 'Sick') NOT NULL,
                NOTES TEXT,
                IS_APPROVED TINYINT(1) DEFAULT NULL,
                APPROVER_ID INT DEFAULT NULL,
                REQUESTED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
                APPROVED_AT DATETIME DEFAULT NULL,
                APPROVAL_NOTES TEXT,
                CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
                UPDATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_user_id (USER_ID),
                INDEX idx_leave_date (LEAVE_DATE),
                INDEX idx_is_approved (IS_APPROVED)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ attendance_leave table created/verified")


def create_attendance_compoff_table():
    """Create the attendance_compoff table"""
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance_compoff (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                USER_ID INT NOT NULL,
                SUNDAY_DATE DATE NOT NULL,
                WORK_PURPOSE VARCHAR(500) NOT NULL,
                COMPOFF_DATE DATE DEFAULT NULL,
                NO_COMPOFF BOOLEAN DEFAULT 0,
                NOTES TEXT,
                IS_APPROVED TINYINT(1) DEFAULT NULL,
                APPROVER_ID INT DEFAULT NULL,
                REQUESTED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
                APPROVED_AT DATETIME DEFAULT NULL,
                APPROVAL_NOTES TEXT,
                CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
                UPDATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_user_id (USER_ID),
                INDEX idx_sunday_date (SUNDAY_DATE),
                INDEX idx_is_approved (IS_APPROVED)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ attendance_compoff table created/verified")


def create_attendance_wfh_table():
    """Create the attendance_wfh table"""
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance_wfh (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                USER_ID INT NOT NULL,
                WFH_DATE DATE NOT NULL,
                REASON VARCHAR(500) NOT NULL,
                NOTES TEXT,
                IS_APPROVED TINYINT(1) DEFAULT NULL,
                APPROVER_ID INT DEFAULT NULL,
                REQUESTED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
                APPROVED_AT DATETIME DEFAULT NULL,
                APPROVAL_NOTES TEXT,
                CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
                UPDATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_user_id (USER_ID),
                INDEX idx_wfh_date (WFH_DATE),
                INDEX idx_is_approved (IS_APPROVED)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ attendance_wfh table created/verified")


def create_column_preferences_table():
    """Create the user_column_preferences table"""
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_column_preferences (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                USER_ID INT NOT NULL,
                TABLE_NAME VARCHAR(50) NOT NULL,
                COLUMN_ORDER JSON NOT NULL,
                CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
                UPDATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE KEY unique_user_table (USER_ID, TABLE_NAME),
                INDEX idx_user_id (USER_ID)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ user_column_preferences table created/verified")


def show_table_info():
    """Show information about created tables"""
    tables = ['attendance_leave', 'attendance_compoff', 'attendance_wfh', 'user_column_preferences']
    
    print("\n" + "="*50)
    print("TABLE SUMMARY")
    print("="*50)
    
    with connection.cursor() as cursor:
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"{table}: {count} records")
            except:
                print(f"{table}: table not found")
    
    print("="*50)


def main():
    print("\n" + "="*50)
    print("SmartLogX - Attendance Tables Setup")
    print("="*50 + "\n")
    
    try:
        create_attendance_leave_table()
        create_attendance_compoff_table()
        create_attendance_wfh_table()
        create_column_preferences_table()
        
        show_table_info()
        
        print("\n✓ Setup complete!")
        print("\nAttendance Modules:")
        print("  - Leave Information: /user/attendance/leave/")
        print("  - Comp-Off Information: /user/attendance/compoff/")
        print("  - WFH Information: /user/attendance/wfh/")
        print("\nFeatures:")
        print("  - Month-wise tables with auto-navigation")
        print("  - Draggable columns with persistent order")
        print("  - Slide-in forms for Add/Edit")
        print("  - Admin approval workflow\n")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
