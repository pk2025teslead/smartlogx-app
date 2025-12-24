"""
SmartLogX User Panel Models
Raw SQL operations for user logs and attendance
"""

from django.db import connection
from datetime import datetime, date
import random
import string


# ============================================
# User Logs Raw SQL Operations
# ============================================

def get_user_logs_by_month(user_id, year, month):
    """Get all logs for a user in a specific month"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                ul.ID, ul.USER_ID, ul.PROJECT_TITLE, ul.LOG_HEADING, 
                ul.LOG_DETAILS, ul.LOG_DATE, ul.SESSION_TYPE,
                ul.APPROVAL_REQUIRED, ul.APPROVAL_CODE, ul.CREATED_AT
            FROM user_logs ul
            WHERE ul.USER_ID = %s 
            AND YEAR(ul.LOG_DATE) = %s 
            AND MONTH(ul.LOG_DATE) = %s
            ORDER BY ul.LOG_DATE DESC, ul.CREATED_AT DESC
        """, [user_id, year, month])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_log_by_id(log_id, user_id=None):
    """Get a specific log by ID"""
    with connection.cursor() as cursor:
        if user_id:
            cursor.execute("""
                SELECT 
                    ID, USER_ID, PROJECT_TITLE, LOG_HEADING, 
                    LOG_DETAILS, LOG_DATE, SESSION_TYPE,
                    APPROVAL_REQUIRED, APPROVAL_CODE, CREATED_AT, UPDATED_AT
                FROM user_logs
                WHERE ID = %s AND USER_ID = %s
            """, [log_id, user_id])
        else:
            cursor.execute("""
                SELECT 
                    ID, USER_ID, PROJECT_TITLE, LOG_HEADING, 
                    LOG_DETAILS, LOG_DATE, SESSION_TYPE,
                    APPROVAL_REQUIRED, APPROVAL_CODE, CREATED_AT, UPDATED_AT
                FROM user_logs
                WHERE ID = %s
            """, [log_id])
        row = cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))
    return None


def create_user_log(user_id, project_title, log_heading, log_details, log_date, session_type, approval_required=False, approval_code=None):
    """Create a new user log entry"""
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO user_logs 
            (USER_ID, PROJECT_TITLE, LOG_HEADING, LOG_DETAILS, LOG_DATE, SESSION_TYPE, 
             APPROVAL_REQUIRED, APPROVAL_CODE, CREATED_AT, UPDATED_AT)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        """, [user_id, project_title, log_heading, log_details, log_date, session_type, 
              approval_required, approval_code])
        return cursor.lastrowid


def update_user_log(log_id, user_id, project_title, log_heading, log_details, session_type):
    """Update an existing log"""
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE user_logs
            SET PROJECT_TITLE = %s, LOG_HEADING = %s, LOG_DETAILS = %s, 
                SESSION_TYPE = %s, UPDATED_AT = NOW()
            WHERE ID = %s AND USER_ID = %s
        """, [project_title, log_heading, log_details, session_type, log_id, user_id])
        return cursor.rowcount


def delete_user_log(log_id, user_id):
    """Delete a log entry"""
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM user_logs WHERE ID = %s AND USER_ID = %s", [log_id, user_id])
        return cursor.rowcount


def get_user_log_stats(user_id, year, month):
    """Get log statistics for a user in a month"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                COUNT(*) as total_logs,
                SUM(CASE WHEN SESSION_TYPE = 'First Half' THEN 1 ELSE 0 END) as first_half_count,
                SUM(CASE WHEN SESSION_TYPE = 'Second Half' THEN 1 ELSE 0 END) as second_half_count,
                SUM(CASE WHEN APPROVAL_REQUIRED = 1 THEN 1 ELSE 0 END) as approval_count
            FROM user_logs
            WHERE USER_ID = %s AND YEAR(LOG_DATE) = %s AND MONTH(LOG_DATE) = %s
        """, [user_id, year, month])
        row = cursor.fetchone()
        if row:
            return {
                'total_logs': row[0] or 0,
                'first_half_count': row[1] or 0,
                'second_half_count': row[2] or 0,
                'approval_count': row[3] or 0
            }
    return {'total_logs': 0, 'first_half_count': 0, 'second_half_count': 0, 'approval_count': 0}


# ============================================
# Approval Code Management
# ============================================

def generate_approval_code():
    """Generate a 6-digit random approval code"""
    return ''.join(random.choices(string.digits, k=6))


def store_approval_code(user_id, code, session_type):
    """Store approval code temporarily"""
    with connection.cursor() as cursor:
        # Delete any existing codes for this user
        cursor.execute("DELETE FROM approval_codes WHERE USER_ID = %s", [user_id])
        # Insert new code with expiry (15 minutes)
        cursor.execute("""
            INSERT INTO approval_codes (USER_ID, CODE, SESSION_TYPE, CREATED_AT, EXPIRES_AT)
            VALUES (%s, %s, %s, NOW(), DATE_ADD(NOW(), INTERVAL 15 MINUTE))
        """, [user_id, code, session_type])
        return cursor.lastrowid


def verify_approval_code(user_id, code):
    """Verify if the approval code is valid and not expired"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ID, CODE, SESSION_TYPE, EXPIRES_AT
            FROM approval_codes
            WHERE USER_ID = %s AND CODE = %s AND EXPIRES_AT > NOW()
        """, [user_id, code])
        row = cursor.fetchone()
        if row:
            # Delete the code after verification
            cursor.execute("DELETE FROM approval_codes WHERE ID = %s", [row[0]])
            return {'valid': True, 'session_type': row[2]}
    return {'valid': False}


def get_admin_email():
    """Get admin email for sending approval codes"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EMAIL FROM users_master WHERE ROLE = 'IT COORDINATOR' LIMIT 1
        """)
        row = cursor.fetchone()
        if row:
            return row[0]
    return None


# ============================================
# Projects List (for dropdown)
# ============================================

def get_user_projects(user_id):
    """Get distinct projects used by a user"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT PROJECT_TITLE
            FROM user_logs
            WHERE USER_ID = %s
            ORDER BY PROJECT_TITLE
        """, [user_id])
        return [row[0] for row in cursor.fetchall()]


def get_all_projects():
    """Get all available projects"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ID, PROJECT_NAME, PROJECT_CODE
            FROM projects
            WHERE IS_ACTIVE = 1
            ORDER BY PROJECT_NAME
        """)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
