"""
SmartLogX Leave Management Module - Database Setup Script
Run this script to create the required tables for the leave module.

Usage:
    python setup_leave_module.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartlogx.settings')
django.setup()

from django.db import connection


def create_leave_tables():
    """Create the leave management tables"""
    
    print("=" * 60)
    print("SmartLogX Leave Management Module - Database Setup")
    print("=" * 60)
    
    with connection.cursor() as cursor:
        # Check if table already exists
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_schema = DATABASE() AND table_name = 'attendance_leave_v2'
        """)
        if cursor.fetchone()[0] > 0:
            print("\n⚠️  Table 'attendance_leave_v2' already exists.")
            response = input("Do you want to drop and recreate? (y/N): ")
            if response.lower() != 'y':
                print("Skipping table creation.")
                return
            cursor.execute("DROP TABLE IF EXISTS attendance_leave_audit")
            cursor.execute("DROP TABLE IF EXISTS attendance_leave_v2")
            print("Dropped existing tables.")
        
        print("\n📦 Creating attendance_leave_v2 table...")
        cursor.execute("""
            CREATE TABLE attendance_leave_v2 (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                leave_date DATE NOT NULL,
                leave_type VARCHAR(50) NOT NULL COMMENT 'PLANNED / CASUAL / EMERGENCY / SICK',
                notes TEXT,
                status VARCHAR(20) NOT NULL DEFAULT 'PENDING' COMMENT 'PENDING / APPROVED / REJECTED / CANCELLED',
                is_editable BOOLEAN NOT NULL DEFAULT TRUE COMMENT 'Convenience flag for edit window',
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                editable_until DATETIME NOT NULL COMMENT 'created_at + 10 minutes',
                updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                created_by INT NOT NULL COMMENT 'User who created the request',
                approved_by INT NULL COMMENT 'Admin who approved/rejected',
                approved_at DATETIME NULL,
                approval_notes TEXT NULL COMMENT 'Admin notes for approval/rejection',
                email_sent_admin BOOLEAN DEFAULT FALSE COMMENT 'Email sent to admin on create',
                email_sent_user BOOLEAN DEFAULT FALSE COMMENT 'Email sent to user on approve/reject',
                INDEX idx_user_id (user_id),
                INDEX idx_status (status),
                INDEX idx_leave_date (leave_date),
                INDEX idx_created_at (created_at),
                INDEX idx_editable_until (editable_until),
                CONSTRAINT fk_leave_user FOREIGN KEY (user_id) REFERENCES users_master(ID) ON DELETE CASCADE,
                CONSTRAINT fk_leave_creator FOREIGN KEY (created_by) REFERENCES users_master(ID) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ Created attendance_leave_v2 table")
        
        print("\n📦 Creating attendance_leave_audit table...")
        cursor.execute("""
            CREATE TABLE attendance_leave_audit (
                id INT AUTO_INCREMENT PRIMARY KEY,
                leave_id INT NOT NULL,
                action VARCHAR(50) NOT NULL COMMENT 'CREATED / EDITED / APPROVED / REJECTED / CANCELLED / DELETED',
                actor_id INT NOT NULL COMMENT 'User who performed the action',
                actor_role VARCHAR(50) NOT NULL COMMENT 'USER / ADMIN',
                actor_name VARCHAR(255) NULL COMMENT 'Cached actor name for display',
                old_data JSON NULL COMMENT 'Previous values before change',
                new_data JSON NULL COMMENT 'New values after change',
                reason TEXT NULL COMMENT 'Reason for action (e.g., rejection reason)',
                ip_address VARCHAR(45) NULL COMMENT 'IP address of actor',
                user_agent TEXT NULL COMMENT 'Browser user agent',
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_leave_id (leave_id),
                INDEX idx_actor_id (actor_id),
                INDEX idx_action (action),
                INDEX idx_created_at (created_at),
                CONSTRAINT fk_audit_leave FOREIGN KEY (leave_id) REFERENCES attendance_leave_v2(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✅ Created attendance_leave_audit table")
        
        print("\n📦 Creating view vw_leave_details...")
        cursor.execute("""
            CREATE OR REPLACE VIEW vw_leave_details AS
            SELECT 
                l.id,
                l.user_id,
                l.leave_date,
                l.leave_type,
                l.notes,
                l.status,
                l.is_editable,
                l.created_at,
                l.editable_until,
                l.updated_at,
                l.created_by,
                l.approved_by,
                l.approved_at,
                l.approval_notes,
                l.email_sent_admin,
                l.email_sent_user,
                u.EMP_ID as emp_id,
                u.EMP_NAME as emp_name,
                u.EMAIL as user_email,
                u.MOBILE_NUMBER as user_mobile,
                a.EMP_NAME as approver_name,
                GREATEST(0, TIMESTAMPDIFF(SECOND, NOW(), l.editable_until)) as edit_seconds_remaining,
                CASE 
                    WHEN l.status = 'PENDING' AND NOW() <= l.editable_until THEN TRUE 
                    ELSE FALSE 
                END as is_currently_editable
            FROM attendance_leave_v2 l
            JOIN users_master u ON l.user_id = u.ID
            LEFT JOIN users_master a ON l.approved_by = a.ID
        """)
        print("✅ Created vw_leave_details view")
        
        print("\n" + "=" * 60)
        print("✅ Leave Management Module setup complete!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Access user panel: /user/attendance/leave/")
        print("2. Access admin panel: /adminpanel/attendance/leave/")
        print("3. Configure email settings in settings.py")
        print("4. Uncomment email.send() in adminpanel/leave_emails.py")


def migrate_from_old_table():
    """Migrate data from old attendance_leave table"""
    
    print("\n📦 Migrating data from attendance_leave...")
    
    with connection.cursor() as cursor:
        # Check if old table exists
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_schema = DATABASE() AND table_name = 'attendance_leave'
        """)
        if cursor.fetchone()[0] == 0:
            print("⚠️  Old table 'attendance_leave' not found. Skipping migration.")
            return
        
        # Count records
        cursor.execute("SELECT COUNT(*) FROM attendance_leave")
        count = cursor.fetchone()[0]
        print(f"Found {count} records to migrate.")
        
        if count == 0:
            return
        
        response = input("Do you want to migrate these records? (y/N): ")
        if response.lower() != 'y':
            print("Skipping migration.")
            return
        
        # Migrate data
        cursor.execute("""
            INSERT INTO attendance_leave_v2 
            (user_id, leave_date, leave_type, notes, status, is_editable, 
             created_at, editable_until, updated_at, created_by, approved_by, 
             approved_at, approval_notes)
            SELECT 
                USER_ID, 
                LEAVE_DATE, 
                LEAVE_TYPE, 
                NOTES, 
                CASE 
                    WHEN IS_APPROVED = 1 THEN 'APPROVED' 
                    WHEN IS_APPROVED = 0 THEN 'REJECTED' 
                    ELSE 'PENDING' 
                END,
                FALSE,
                COALESCE(REQUESTED_AT, CREATED_AT, NOW()),
                DATE_ADD(COALESCE(REQUESTED_AT, CREATED_AT, NOW()), INTERVAL 10 MINUTE),
                COALESCE(UPDATED_AT, NOW()),
                USER_ID,
                APPROVER_ID,
                APPROVED_AT,
                APPROVAL_NOTES
            FROM attendance_leave
        """)
        
        print(f"✅ Migrated {cursor.rowcount} records successfully!")


if __name__ == '__main__':
    try:
        create_leave_tables()
        
        response = input("\nDo you want to migrate data from old table? (y/N): ")
        if response.lower() == 'y':
            migrate_from_old_table()
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
