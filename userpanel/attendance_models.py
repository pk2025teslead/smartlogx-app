"""
SmartLogX Attendance Management - Raw SQL Models
Leave, Comp-Off, WFH Operations
"""

from django.db import connection
from datetime import datetime, date
import json


# ============================================
# LEAVE INFORMATION - Raw SQL Operations
# ============================================

def get_leaves_by_month(user_id, year, month):
    """Get all leave records for a user in a specific month"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                l.ID, l.USER_ID, l.LEAVE_DATE, l.LEAVE_TYPE, l.NOTES,
                l.IS_APPROVED, l.APPROVER_ID, l.REQUESTED_AT, l.APPROVED_AT,
                l.APPROVAL_NOTES, l.CREATED_AT,
                u.EMP_NAME as APPROVER_NAME
            FROM attendance_leave l
            LEFT JOIN users_master u ON l.APPROVER_ID = u.ID
            WHERE l.USER_ID = %s 
            AND YEAR(l.LEAVE_DATE) = %s 
            AND MONTH(l.LEAVE_DATE) = %s
            ORDER BY l.LEAVE_DATE DESC, l.CREATED_AT DESC
        """, [user_id, year, month])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_leave_by_id(leave_id, user_id=None):
    """Get a specific leave record"""
    with connection.cursor() as cursor:
        if user_id:
            cursor.execute("""
                SELECT * FROM attendance_leave WHERE ID = %s AND USER_ID = %s
            """, [leave_id, user_id])
        else:
            cursor.execute("SELECT * FROM attendance_leave WHERE ID = %s", [leave_id])
        row = cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))
    return None


def create_leave(user_id, leave_date, leave_type, notes=None):
    """Create a new leave request"""
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO attendance_leave 
            (USER_ID, LEAVE_DATE, LEAVE_TYPE, NOTES, IS_APPROVED, REQUESTED_AT, CREATED_AT, UPDATED_AT)
            VALUES (%s, %s, %s, %s, NULL, NOW(), NOW(), NOW())
        """, [user_id, leave_date, leave_type, notes])
        return cursor.lastrowid


def update_leave(leave_id, user_id, leave_date, leave_type, notes=None):
    """Update an existing leave request (only if not yet approved)"""
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE attendance_leave
            SET LEAVE_DATE = %s, LEAVE_TYPE = %s, NOTES = %s, UPDATED_AT = NOW()
            WHERE ID = %s AND USER_ID = %s AND IS_APPROVED IS NULL
        """, [leave_date, leave_type, notes, leave_id, user_id])
        return cursor.rowcount


def delete_leave(leave_id, user_id):
    """Delete a leave request (only if not yet approved)"""
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM attendance_leave 
            WHERE ID = %s AND USER_ID = %s AND IS_APPROVED IS NULL
        """, [leave_id, user_id])
        return cursor.rowcount


def approve_leave(leave_id, approver_id, is_approved, approval_notes=None):
    """Admin approve/reject a leave request"""
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE attendance_leave
            SET IS_APPROVED = %s, APPROVER_ID = %s, APPROVED_AT = NOW(), 
                APPROVAL_NOTES = %s, UPDATED_AT = NOW()
            WHERE ID = %s
        """, [is_approved, approver_id, approval_notes, leave_id])
        return cursor.rowcount


def get_leave_stats(user_id, year, month):
    """Get leave statistics for a user"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN IS_APPROVED = 1 THEN 1 ELSE 0 END) as approved,
                SUM(CASE WHEN IS_APPROVED = 0 THEN 1 ELSE 0 END) as rejected,
                SUM(CASE WHEN IS_APPROVED IS NULL THEN 1 ELSE 0 END) as pending
            FROM attendance_leave
            WHERE USER_ID = %s AND YEAR(LEAVE_DATE) = %s AND MONTH(LEAVE_DATE) = %s
        """, [user_id, year, month])
        row = cursor.fetchone()
        return {
            'total': row[0] or 0,
            'approved': row[1] or 0,
            'rejected': row[2] or 0,
            'pending': row[3] or 0
        }


# ============================================
# COMP-OFF INFORMATION - Raw SQL Operations
# ============================================

def get_compoffs_by_month(user_id, year, month):
    """Get all comp-off records for a user in a specific month"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                c.ID, c.USER_ID, c.SUNDAY_DATE, c.WORK_PURPOSE, c.COMPOFF_DATE,
                c.NO_COMPOFF, c.NOTES, c.IS_APPROVED, c.APPROVER_ID, 
                c.REQUESTED_AT, c.APPROVED_AT, c.APPROVAL_NOTES, c.CREATED_AT,
                u.EMP_NAME as APPROVER_NAME
            FROM attendance_compoff c
            LEFT JOIN users_master u ON c.APPROVER_ID = u.ID
            WHERE c.USER_ID = %s 
            AND YEAR(c.SUNDAY_DATE) = %s 
            AND MONTH(c.SUNDAY_DATE) = %s
            ORDER BY c.SUNDAY_DATE DESC, c.CREATED_AT DESC
        """, [user_id, year, month])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_compoff_by_id(compoff_id, user_id=None):
    """Get a specific comp-off record"""
    with connection.cursor() as cursor:
        if user_id:
            cursor.execute("""
                SELECT * FROM attendance_compoff WHERE ID = %s AND USER_ID = %s
            """, [compoff_id, user_id])
        else:
            cursor.execute("SELECT * FROM attendance_compoff WHERE ID = %s", [compoff_id])
        row = cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))
    return None


def create_compoff(user_id, sunday_date, work_purpose, compoff_date=None, no_compoff=False, notes=None):
    """Create a new comp-off request"""
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO attendance_compoff 
            (USER_ID, SUNDAY_DATE, WORK_PURPOSE, COMPOFF_DATE, NO_COMPOFF, NOTES, 
             IS_APPROVED, REQUESTED_AT, CREATED_AT, UPDATED_AT)
            VALUES (%s, %s, %s, %s, %s, %s, NULL, NOW(), NOW(), NOW())
        """, [user_id, sunday_date, work_purpose, compoff_date, no_compoff, notes])
        return cursor.lastrowid


def update_compoff(compoff_id, user_id, sunday_date, work_purpose, compoff_date=None, no_compoff=False, notes=None):
    """Update an existing comp-off request"""
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE attendance_compoff
            SET SUNDAY_DATE = %s, WORK_PURPOSE = %s, COMPOFF_DATE = %s, 
                NO_COMPOFF = %s, NOTES = %s, UPDATED_AT = NOW()
            WHERE ID = %s AND USER_ID = %s AND IS_APPROVED IS NULL
        """, [sunday_date, work_purpose, compoff_date, no_compoff, notes, compoff_id, user_id])
        return cursor.rowcount


def delete_compoff(compoff_id, user_id):
    """Delete a comp-off request"""
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM attendance_compoff 
            WHERE ID = %s AND USER_ID = %s AND IS_APPROVED IS NULL
        """, [compoff_id, user_id])
        return cursor.rowcount


def approve_compoff(compoff_id, approver_id, is_approved, approval_notes=None):
    """Admin approve/reject a comp-off request"""
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE attendance_compoff
            SET IS_APPROVED = %s, APPROVER_ID = %s, APPROVED_AT = NOW(), 
                APPROVAL_NOTES = %s, UPDATED_AT = NOW()
            WHERE ID = %s
        """, [is_approved, approver_id, approval_notes, compoff_id])
        return cursor.rowcount


def get_compoff_stats(user_id, year, month):
    """Get comp-off statistics"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN IS_APPROVED = 1 THEN 1 ELSE 0 END) as approved,
                SUM(CASE WHEN IS_APPROVED = 0 THEN 1 ELSE 0 END) as rejected,
                SUM(CASE WHEN IS_APPROVED IS NULL THEN 1 ELSE 0 END) as pending
            FROM attendance_compoff
            WHERE USER_ID = %s AND YEAR(SUNDAY_DATE) = %s AND MONTH(SUNDAY_DATE) = %s
        """, [user_id, year, month])
        row = cursor.fetchone()
        return {
            'total': row[0] or 0,
            'approved': row[1] or 0,
            'rejected': row[2] or 0,
            'pending': row[3] or 0
        }


# ============================================
# WFH INFORMATION - Raw SQL Operations
# ============================================

def get_wfh_by_month(user_id, year, month):
    """Get all WFH records for a user in a specific month"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                w.ID, w.USER_ID, w.WFH_DATE, w.REASON, w.NOTES,
                w.IS_APPROVED, w.APPROVER_ID, w.REQUESTED_AT, w.APPROVED_AT,
                w.APPROVAL_NOTES, w.CREATED_AT,
                u.EMP_NAME as APPROVER_NAME
            FROM attendance_wfh w
            LEFT JOIN users_master u ON w.APPROVER_ID = u.ID
            WHERE w.USER_ID = %s 
            AND YEAR(w.WFH_DATE) = %s 
            AND MONTH(w.WFH_DATE) = %s
            ORDER BY w.WFH_DATE DESC, w.CREATED_AT DESC
        """, [user_id, year, month])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_wfh_by_id(wfh_id, user_id=None):
    """Get a specific WFH record"""
    with connection.cursor() as cursor:
        if user_id:
            cursor.execute("""
                SELECT * FROM attendance_wfh WHERE ID = %s AND USER_ID = %s
            """, [wfh_id, user_id])
        else:
            cursor.execute("SELECT * FROM attendance_wfh WHERE ID = %s", [wfh_id])
        row = cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))
    return None


def create_wfh(user_id, wfh_date, reason, notes=None):
    """Create a new WFH request"""
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO attendance_wfh 
            (USER_ID, WFH_DATE, REASON, NOTES, IS_APPROVED, REQUESTED_AT, CREATED_AT, UPDATED_AT)
            VALUES (%s, %s, %s, %s, NULL, NOW(), NOW(), NOW())
        """, [user_id, wfh_date, reason, notes])
        return cursor.lastrowid


def update_wfh(wfh_id, user_id, wfh_date, reason, notes=None):
    """Update an existing WFH request"""
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE attendance_wfh
            SET WFH_DATE = %s, REASON = %s, NOTES = %s, UPDATED_AT = NOW()
            WHERE ID = %s AND USER_ID = %s AND IS_APPROVED IS NULL
        """, [wfh_date, reason, notes, wfh_id, user_id])
        return cursor.rowcount


def delete_wfh(wfh_id, user_id):
    """Delete a WFH request"""
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM attendance_wfh 
            WHERE ID = %s AND USER_ID = %s AND IS_APPROVED IS NULL
        """, [wfh_id, user_id])
        return cursor.rowcount


def approve_wfh(wfh_id, approver_id, is_approved, approval_notes=None):
    """Admin approve/reject a WFH request"""
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE attendance_wfh
            SET IS_APPROVED = %s, APPROVER_ID = %s, APPROVED_AT = NOW(), 
                APPROVAL_NOTES = %s, UPDATED_AT = NOW()
            WHERE ID = %s
        """, [is_approved, approver_id, approval_notes, wfh_id])
        return cursor.rowcount


def get_wfh_stats(user_id, year, month):
    """Get WFH statistics"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN IS_APPROVED = 1 THEN 1 ELSE 0 END) as approved,
                SUM(CASE WHEN IS_APPROVED = 0 THEN 1 ELSE 0 END) as rejected,
                SUM(CASE WHEN IS_APPROVED IS NULL THEN 1 ELSE 0 END) as pending
            FROM attendance_wfh
            WHERE USER_ID = %s AND YEAR(WFH_DATE) = %s AND MONTH(WFH_DATE) = %s
        """, [user_id, year, month])
        row = cursor.fetchone()
        return {
            'total': row[0] or 0,
            'approved': row[1] or 0,
            'rejected': row[2] or 0,
            'pending': row[3] or 0
        }


# ============================================
# COLUMN PREFERENCES - Raw SQL Operations
# ============================================

def get_column_order(user_id, table_name):
    """Get saved column order for a table"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COLUMN_ORDER FROM user_column_preferences
            WHERE USER_ID = %s AND TABLE_NAME = %s
        """, [user_id, table_name])
        row = cursor.fetchone()
        if row and row[0]:
            return json.loads(row[0]) if isinstance(row[0], str) else row[0]
    return None


def save_column_order(user_id, table_name, column_order):
    """Save column order for a table"""
    column_json = json.dumps(column_order)
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO user_column_preferences (USER_ID, TABLE_NAME, COLUMN_ORDER, CREATED_AT, UPDATED_AT)
            VALUES (%s, %s, %s, NOW(), NOW())
            ON DUPLICATE KEY UPDATE COLUMN_ORDER = %s, UPDATED_AT = NOW()
        """, [user_id, table_name, column_json, column_json])
        return cursor.rowcount


# ============================================
# ADMIN: Get All Pending Requests
# ============================================

def get_all_pending_leaves():
    """Get all pending leave requests (for admin)"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT l.*, u.EMP_NAME, u.EMP_ID, u.EMAIL
            FROM attendance_leave l
            JOIN users_master u ON l.USER_ID = u.ID
            WHERE l.IS_APPROVED IS NULL
            ORDER BY l.REQUESTED_AT DESC
        """)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_all_pending_compoffs():
    """Get all pending comp-off requests (for admin)"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.*, u.EMP_NAME, u.EMP_ID, u.EMAIL
            FROM attendance_compoff c
            JOIN users_master u ON c.USER_ID = u.ID
            WHERE c.IS_APPROVED IS NULL
            ORDER BY c.REQUESTED_AT DESC
        """)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_all_pending_wfh():
    """Get all pending WFH requests (for admin)"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT w.*, u.EMP_NAME, u.EMP_ID, u.EMAIL
            FROM attendance_wfh w
            JOIN users_master u ON w.USER_ID = u.ID
            WHERE w.IS_APPROVED IS NULL
            ORDER BY w.REQUESTED_AT DESC
        """)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
