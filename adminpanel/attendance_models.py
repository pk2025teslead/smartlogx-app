"""
SmartLogX Admin Panel - Attendance Management Raw SQL Models
Leave, Comp-Off, WFH Operations for Admin
"""

from django.db import connection
from datetime import datetime, date
import json


def dictfetchall(cursor):
    """Return all rows from a cursor as a list of dicts"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def dictfetchone(cursor):
    """Return one row from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    return dict(zip(columns, row)) if row else None


# ============================================
# LEAVE MANAGEMENT - Admin Operations
# ============================================

def get_all_leaves_by_month(year, month):
    """Get all leave records for a specific month (admin view)"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                l.ID, l.USER_ID, l.LEAVE_DATE, l.LEAVE_TYPE, l.NOTES,
                l.IS_APPROVED, l.APPROVER_ID, l.REQUESTED_AT, l.APPROVED_AT,
                l.APPROVAL_NOTES, l.CREATED_AT, l.UPDATED_AT,
                u.EMP_ID, u.EMP_NAME, u.EMAIL as USER_EMAIL,
                a.EMP_NAME as APPROVER_NAME
            FROM attendance_leave l
            JOIN users_master u ON l.USER_ID = u.ID
            LEFT JOIN users_master a ON l.APPROVER_ID = a.ID
            WHERE YEAR(l.LEAVE_DATE) = %s AND MONTH(l.LEAVE_DATE) = %s
            ORDER BY l.LEAVE_DATE DESC, l.CREATED_AT DESC
        """, [year, month])
        return dictfetchall(cursor)


def get_leave_by_id(leave_id):
    """Get a specific leave record"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                l.*, u.EMP_ID, u.EMP_NAME, u.EMAIL as USER_EMAIL,
                a.EMP_NAME as APPROVER_NAME
            FROM attendance_leave l
            JOIN users_master u ON l.USER_ID = u.ID
            LEFT JOIN users_master a ON l.APPROVER_ID = a.ID
            WHERE l.ID = %s
        """, [leave_id])
        return dictfetchone(cursor)


def update_leave_admin(leave_id, leave_date, leave_type, notes):
    """Admin update leave record"""
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE attendance_leave
            SET LEAVE_DATE = %s, LEAVE_TYPE = %s, NOTES = %s, UPDATED_AT = NOW()
            WHERE ID = %s
        """, [leave_date, leave_type, notes, leave_id])
        return cursor.rowcount


def delete_leave_admin(leave_id):
    """Admin delete leave record"""
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM attendance_leave WHERE ID = %s", [leave_id])
        return cursor.rowcount


def approve_reject_leave(leave_id, approver_id, is_approved, approval_notes=None):
    """Admin approve or reject leave"""
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE attendance_leave
            SET IS_APPROVED = %s, APPROVER_ID = %s, APPROVED_AT = NOW(), 
                APPROVAL_NOTES = %s, UPDATED_AT = NOW()
            WHERE ID = %s
        """, [is_approved, approver_id, approval_notes, leave_id])
        return cursor.rowcount


def get_leave_stats(year, month):
    """Get leave statistics for dashboard"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN IS_APPROVED = 1 THEN 1 ELSE 0 END) as approved,
                SUM(CASE WHEN IS_APPROVED = 0 THEN 1 ELSE 0 END) as rejected,
                SUM(CASE WHEN IS_APPROVED IS NULL THEN 1 ELSE 0 END) as pending
            FROM attendance_leave
            WHERE YEAR(LEAVE_DATE) = %s AND MONTH(LEAVE_DATE) = %s
        """, [year, month])
        result = dictfetchone(cursor)
        # Convert Decimal to int for JSON serialization
        return {k: int(v or 0) for k, v in result.items()} if result else {'total': 0, 'approved': 0, 'rejected': 0, 'pending': 0}


def get_recent_leaves(limit=5):
    """Get recent leave requests"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT l.*, u.EMP_NAME, u.EMP_ID
            FROM attendance_leave l
            JOIN users_master u ON l.USER_ID = u.ID
            ORDER BY l.CREATED_AT DESC
            LIMIT %s
        """, [limit])
        return dictfetchall(cursor)


# ============================================
# COMP-OFF MANAGEMENT - Admin Operations
# ============================================

def get_all_compoffs_by_month(year, month):
    """Get all comp-off records for a specific month"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                c.ID, c.USER_ID, c.SUNDAY_DATE, c.WORK_PURPOSE, c.COMPOFF_DATE,
                c.NO_COMPOFF, c.NOTES, c.IS_APPROVED, c.APPROVER_ID,
                c.REQUESTED_AT, c.APPROVED_AT, c.APPROVAL_NOTES, c.CREATED_AT,
                u.EMP_ID, u.EMP_NAME, u.EMAIL as USER_EMAIL,
                a.EMP_NAME as APPROVER_NAME
            FROM attendance_compoff c
            JOIN users_master u ON c.USER_ID = u.ID
            LEFT JOIN users_master a ON c.APPROVER_ID = a.ID
            WHERE YEAR(c.SUNDAY_DATE) = %s AND MONTH(c.SUNDAY_DATE) = %s
            ORDER BY c.SUNDAY_DATE DESC, c.CREATED_AT DESC
        """, [year, month])
        return dictfetchall(cursor)


def get_compoff_by_id(compoff_id):
    """Get a specific comp-off record"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                c.*, u.EMP_ID, u.EMP_NAME, u.EMAIL as USER_EMAIL,
                a.EMP_NAME as APPROVER_NAME
            FROM attendance_compoff c
            JOIN users_master u ON c.USER_ID = u.ID
            LEFT JOIN users_master a ON c.APPROVER_ID = a.ID
            WHERE c.ID = %s
        """, [compoff_id])
        return dictfetchone(cursor)


def update_compoff_admin(compoff_id, sunday_date, work_purpose, compoff_date, no_compoff, notes):
    """Admin update comp-off record"""
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE attendance_compoff
            SET SUNDAY_DATE = %s, WORK_PURPOSE = %s, COMPOFF_DATE = %s, 
                NO_COMPOFF = %s, NOTES = %s, UPDATED_AT = NOW()
            WHERE ID = %s
        """, [sunday_date, work_purpose, compoff_date, no_compoff, notes, compoff_id])
        return cursor.rowcount


def delete_compoff_admin(compoff_id):
    """Admin delete comp-off record"""
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM attendance_compoff WHERE ID = %s", [compoff_id])
        return cursor.rowcount


def approve_reject_compoff(compoff_id, approver_id, is_approved, approval_notes=None):
    """Admin approve or reject comp-off"""
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE attendance_compoff
            SET IS_APPROVED = %s, APPROVER_ID = %s, APPROVED_AT = NOW(), 
                APPROVAL_NOTES = %s, UPDATED_AT = NOW()
            WHERE ID = %s
        """, [is_approved, approver_id, approval_notes, compoff_id])
        return cursor.rowcount


def get_compoff_stats(year, month):
    """Get comp-off statistics"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN IS_APPROVED = 1 THEN 1 ELSE 0 END) as approved,
                SUM(CASE WHEN IS_APPROVED = 0 THEN 1 ELSE 0 END) as rejected,
                SUM(CASE WHEN IS_APPROVED IS NULL THEN 1 ELSE 0 END) as pending
            FROM attendance_compoff
            WHERE YEAR(SUNDAY_DATE) = %s AND MONTH(SUNDAY_DATE) = %s
        """, [year, month])
        result = dictfetchone(cursor)
        return {k: int(v or 0) for k, v in result.items()} if result else {'total': 0, 'approved': 0, 'rejected': 0, 'pending': 0}


def get_recent_compoffs(limit=5):
    """Get recent comp-off requests"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.*, u.EMP_NAME, u.EMP_ID
            FROM attendance_compoff c
            JOIN users_master u ON c.USER_ID = u.ID
            ORDER BY c.CREATED_AT DESC
            LIMIT %s
        """, [limit])
        return dictfetchall(cursor)


# ============================================
# WFH MANAGEMENT - Admin Operations
# ============================================

def get_all_wfh_by_month(year, month):
    """Get all WFH records for a specific month"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                w.ID, w.USER_ID, w.WFH_DATE, w.REASON, w.NOTES,
                w.IS_APPROVED, w.APPROVER_ID, w.REQUESTED_AT, w.APPROVED_AT,
                w.APPROVAL_NOTES, w.CREATED_AT,
                u.EMP_ID, u.EMP_NAME, u.EMAIL as USER_EMAIL,
                a.EMP_NAME as APPROVER_NAME
            FROM attendance_wfh w
            JOIN users_master u ON w.USER_ID = u.ID
            LEFT JOIN users_master a ON w.APPROVER_ID = a.ID
            WHERE YEAR(w.WFH_DATE) = %s AND MONTH(w.WFH_DATE) = %s
            ORDER BY w.WFH_DATE DESC, w.CREATED_AT DESC
        """, [year, month])
        return dictfetchall(cursor)


def get_wfh_by_id(wfh_id):
    """Get a specific WFH record"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                w.*, u.EMP_ID, u.EMP_NAME, u.EMAIL as USER_EMAIL,
                a.EMP_NAME as APPROVER_NAME
            FROM attendance_wfh w
            JOIN users_master u ON w.USER_ID = u.ID
            LEFT JOIN users_master a ON w.APPROVER_ID = a.ID
            WHERE w.ID = %s
        """, [wfh_id])
        return dictfetchone(cursor)


def update_wfh_admin(wfh_id, wfh_date, reason, notes):
    """Admin update WFH record"""
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE attendance_wfh
            SET WFH_DATE = %s, REASON = %s, NOTES = %s, UPDATED_AT = NOW()
            WHERE ID = %s
        """, [wfh_date, reason, notes, wfh_id])
        return cursor.rowcount


def delete_wfh_admin(wfh_id):
    """Admin delete WFH record"""
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM attendance_wfh WHERE ID = %s", [wfh_id])
        return cursor.rowcount


def approve_reject_wfh(wfh_id, approver_id, is_approved, approval_notes=None):
    """Admin approve or reject WFH"""
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE attendance_wfh
            SET IS_APPROVED = %s, APPROVER_ID = %s, APPROVED_AT = NOW(), 
                APPROVAL_NOTES = %s, UPDATED_AT = NOW()
            WHERE ID = %s
        """, [is_approved, approver_id, approval_notes, wfh_id])
        return cursor.rowcount


def get_wfh_stats(year, month):
    """Get WFH statistics"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN IS_APPROVED = 1 THEN 1 ELSE 0 END) as approved,
                SUM(CASE WHEN IS_APPROVED = 0 THEN 1 ELSE 0 END) as rejected,
                SUM(CASE WHEN IS_APPROVED IS NULL THEN 1 ELSE 0 END) as pending
            FROM attendance_wfh
            WHERE YEAR(WFH_DATE) = %s AND MONTH(WFH_DATE) = %s
        """, [year, month])
        result = dictfetchone(cursor)
        return {k: int(v or 0) for k, v in result.items()} if result else {'total': 0, 'approved': 0, 'rejected': 0, 'pending': 0}


def get_recent_wfh(limit=5):
    """Get recent WFH requests"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT w.*, u.EMP_NAME, u.EMP_ID
            FROM attendance_wfh w
            JOIN users_master u ON w.USER_ID = u.ID
            ORDER BY w.CREATED_AT DESC
            LIMIT %s
        """, [limit])
        return dictfetchall(cursor)


# ============================================
# LOG MANAGEMENT - Admin Operations
# ============================================

def get_all_logs_by_month(year, month):
    """Get all user logs for a specific month"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                l.ID, l.USER_ID, l.PROJECT_TITLE, l.LOG_HEADING, l.LOG_DETAILS,
                l.LOG_DATE, l.SESSION_TYPE, l.APPROVAL_REQUIRED, l.CREATED_AT,
                u.EMP_ID, u.EMP_NAME, u.EMAIL as USER_EMAIL
            FROM user_logs l
            JOIN users_master u ON l.USER_ID = u.ID
            WHERE YEAR(l.LOG_DATE) = %s AND MONTH(l.LOG_DATE) = %s
            ORDER BY l.LOG_DATE DESC, l.CREATED_AT DESC
        """, [year, month])
        return dictfetchall(cursor)


def get_log_by_id(log_id):
    """Get a specific log record"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                l.*, u.EMP_ID, u.EMP_NAME, u.EMAIL as USER_EMAIL
            FROM user_logs l
            JOIN users_master u ON l.USER_ID = u.ID
            WHERE l.ID = %s
        """, [log_id])
        return dictfetchone(cursor)


def get_log_stats(year, month):
    """Get log statistics"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN SESSION_TYPE = 'First Half' THEN 1 ELSE 0 END) as first_half,
                SUM(CASE WHEN SESSION_TYPE = 'Second Half' THEN 1 ELSE 0 END) as second_half,
                SUM(CASE WHEN APPROVAL_REQUIRED = 1 THEN 1 ELSE 0 END) as with_approval
            FROM user_logs
            WHERE YEAR(LOG_DATE) = %s AND MONTH(LOG_DATE) = %s
        """, [year, month])
        result = dictfetchone(cursor)
        return {k: int(v or 0) for k, v in result.items()} if result else {'total': 0, 'first_half': 0, 'second_half': 0, 'with_approval': 0}


def get_recent_logs(limit=5):
    """Get recent logs"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT l.*, u.EMP_NAME, u.EMP_ID
            FROM user_logs l
            JOIN users_master u ON l.USER_ID = u.ID
            ORDER BY l.CREATED_AT DESC
            LIMIT %s
        """, [limit])
        return dictfetchall(cursor)


# ============================================
# DASHBOARD STATISTICS
# ============================================

def get_dashboard_stats():
    """Get all dashboard statistics"""
    with connection.cursor() as cursor:
        # Total users
        cursor.execute("SELECT COUNT(*) FROM users_master")
        total_users = cursor.fetchone()[0]
        
        # Current month stats
        now = datetime.now()
        year, month = now.year, now.month
        
        # Leaves this month
        cursor.execute("""
            SELECT COUNT(*), 
                   SUM(CASE WHEN IS_APPROVED = 1 THEN 1 ELSE 0 END),
                   SUM(CASE WHEN IS_APPROVED IS NULL THEN 1 ELSE 0 END)
            FROM attendance_leave 
            WHERE YEAR(LEAVE_DATE) = %s AND MONTH(LEAVE_DATE) = %s
        """, [year, month])
        leave_row = cursor.fetchone()
        
        # Comp-offs this month
        cursor.execute("""
            SELECT COUNT(*), 
                   SUM(CASE WHEN IS_APPROVED = 1 THEN 1 ELSE 0 END),
                   SUM(CASE WHEN IS_APPROVED IS NULL THEN 1 ELSE 0 END)
            FROM attendance_compoff 
            WHERE YEAR(SUNDAY_DATE) = %s AND MONTH(SUNDAY_DATE) = %s
        """, [year, month])
        compoff_row = cursor.fetchone()
        
        # WFH this month
        cursor.execute("""
            SELECT COUNT(*), 
                   SUM(CASE WHEN IS_APPROVED = 1 THEN 1 ELSE 0 END),
                   SUM(CASE WHEN IS_APPROVED IS NULL THEN 1 ELSE 0 END)
            FROM attendance_wfh 
            WHERE YEAR(WFH_DATE) = %s AND MONTH(WFH_DATE) = %s
        """, [year, month])
        wfh_row = cursor.fetchone()
        
        # Logs this month
        cursor.execute("""
            SELECT COUNT(*) FROM user_logs 
            WHERE YEAR(LOG_DATE) = %s AND MONTH(LOG_DATE) = %s
        """, [year, month])
        total_logs = cursor.fetchone()[0]
        
        # Convert Decimal to int for JSON serialization
        return {
            'total_users': int(total_users or 0),
            'leaves': {
                'total': int(leave_row[0] or 0),
                'approved': int(leave_row[1] or 0),
                'pending': int(leave_row[2] or 0)
            },
            'compoffs': {
                'total': int(compoff_row[0] or 0),
                'approved': int(compoff_row[1] or 0),
                'pending': int(compoff_row[2] or 0)
            },
            'wfh': {
                'total': int(wfh_row[0] or 0),
                'approved': int(wfh_row[1] or 0),
                'pending': int(wfh_row[2] or 0)
            },
            'logs': {
                'total': int(total_logs or 0)
            }
        }
