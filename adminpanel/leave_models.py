"""
SmartLogX Leave Management Module - Raw SQL Models
Enhanced with 10-minute edit window and audit trail
Timezone: Asia/Kolkata (IST)
"""

from django.db import connection, transaction
from datetime import datetime, timedelta
import pytz
import json
import logging

logger = logging.getLogger(__name__)

IST = pytz.timezone('Asia/Kolkata')
EDIT_WINDOW_MINUTES = 10


def get_ist_now():
    """Get current datetime in IST"""
    return datetime.now(IST)


def format_ist_datetime(dt):
    """Format datetime for display in IST"""
    if dt is None:
        return None
    if isinstance(dt, str):
        return dt
    if dt.tzinfo is None:
        dt = IST.localize(dt)
    return dt.strftime('%d-%b-%Y %H:%M IST')


def dictfetchall(cursor):
    """Return all rows from a cursor as a list of dicts"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def dictfetchone(cursor):
    """Return one row from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    return dict(zip(columns, row)) if row else None


def row_to_json(row_dict):
    """Convert row dict to JSON-serializable format"""
    if row_dict is None:
        return None
    result = {}
    for key, value in row_dict.items():
        if isinstance(value, datetime):
            result[key] = value.isoformat()
        elif isinstance(value, (bytes, bytearray)):
            result[key] = value.decode('utf-8')
        else:
            result[key] = value
    return result


# ============================================
# AUDIT TRAIL FUNCTIONS
# ============================================

def insert_audit(cursor, leave_id, action, actor_id, actor_role, old_data=None, new_data=None, reason=None, ip_address=None, user_agent=None):
    """Insert audit trail record"""
    try:
        # Get actor name
        cursor.execute("SELECT EMP_NAME FROM users_master WHERE ID = %s", [actor_id])
        actor_row = cursor.fetchone()
        actor_name = actor_row[0] if actor_row else 'Unknown'
        
        cursor.execute("""
            INSERT INTO attendance_leave_audit 
            (leave_id, action, actor_id, actor_role, actor_name, old_data, new_data, reason, ip_address, user_agent, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """, [
            leave_id,
            action,
            actor_id,
            actor_role,
            actor_name,
            json.dumps(row_to_json(old_data)) if old_data else None,
            json.dumps(row_to_json(new_data)) if new_data else None,
            reason,
            ip_address,
            user_agent
        ])
        return cursor.lastrowid
    except Exception as e:
        logger.error(f"Failed to insert audit: {e}")
        return None


def get_audit_trail(leave_id, limit=50):
    """Get audit trail for a leave request"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                id, leave_id, action, actor_id, actor_role, actor_name,
                old_data, new_data, reason, ip_address, created_at
            FROM attendance_leave_audit
            WHERE leave_id = %s
            ORDER BY created_at DESC
            LIMIT %s
        """, [leave_id, limit])
        return dictfetchall(cursor)


# ============================================
# LEAVE CRUD OPERATIONS - USER
# ============================================

def calculate_leave_days(from_date_str, to_date_str):
    """Calculate total leave days between two dates (inclusive)"""
    from datetime import datetime
    from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
    to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
    return (to_date - from_date).days + 1


def create_leave(user_id, from_date, to_date, leave_type, notes=None, ip_address=None, user_agent=None):
    """
    Create a new leave request with date range and edit window
    Returns: (leave_id, editable_until, total_days) or raises exception
    """
    now = get_ist_now()
    editable_until = now + timedelta(minutes=EDIT_WINDOW_MINUTES)
    total_days = calculate_leave_days(from_date, to_date)
    
    with transaction.atomic():
        with connection.cursor() as cursor:
            # Insert leave record with date range
            cursor.execute("""
                INSERT INTO attendance_leave_v2 
                (user_id, leave_date, from_date, to_date, total_days, leave_type, notes, status, is_editable, 
                 created_at, editable_until, updated_at, created_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'PENDING', TRUE, %s, %s, %s, %s)
            """, [
                user_id, from_date, from_date, to_date, total_days, leave_type, notes,
                now.strftime('%Y-%m-%d %H:%M:%S'),
                editable_until.strftime('%Y-%m-%d %H:%M:%S'),
                now.strftime('%Y-%m-%d %H:%M:%S'),
                user_id
            ])
            leave_id = cursor.lastrowid
            
            # Get the created record for audit
            cursor.execute("SELECT * FROM attendance_leave_v2 WHERE id = %s", [leave_id])
            new_data = dictfetchone(cursor)
            
            # Insert audit record
            insert_audit(
                cursor, leave_id, 'CREATED', user_id, 'USER',
                old_data=None, new_data=new_data,
                ip_address=ip_address, user_agent=user_agent
            )
            
            return leave_id, editable_until, total_days


def get_leave_by_id(leave_id, user_id=None):
    """Get leave by ID with user details"""
    with connection.cursor() as cursor:
        if user_id:
            cursor.execute("""
                SELECT * FROM vw_leave_details WHERE id = %s AND user_id = %s
            """, [leave_id, user_id])
        else:
            cursor.execute("SELECT * FROM vw_leave_details WHERE id = %s", [leave_id])
        return dictfetchone(cursor)


def get_leave_raw(leave_id):
    """Get raw leave record for updates"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM attendance_leave_v2 WHERE id = %s", [leave_id])
        return dictfetchone(cursor)


def check_edit_window(leave_id, user_id):
    """
    Check if leave is editable by user
    Returns: (is_editable: bool, message: str, seconds_remaining: int)
    """
    now = get_ist_now()
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, user_id, status, editable_until, is_editable
            FROM attendance_leave_v2
            WHERE id = %s
        """, [leave_id])
        row = dictfetchone(cursor)
        
        if not row:
            return False, "Leave request not found", 0
        
        if row['user_id'] != user_id:
            return False, "You are not authorized to edit this request", 0
        
        if row['status'] != 'PENDING':
            return False, f"Cannot edit - status is {row['status']}", 0
        
        editable_until = row['editable_until']
        if isinstance(editable_until, str):
            editable_until = datetime.strptime(editable_until, '%Y-%m-%d %H:%M:%S')
        
        if editable_until.tzinfo is None:
            editable_until = IST.localize(editable_until)
        
        if now > editable_until:
            return False, f"Edit window expired at {format_ist_datetime(editable_until)}", 0
        
        seconds_remaining = int((editable_until - now).total_seconds())
        return True, "Editable", max(0, seconds_remaining)


def update_leave_user(leave_id, user_id, from_date, to_date, leave_type, notes=None, ip_address=None, user_agent=None):
    """
    Update leave request (user) - only within edit window
    Returns: (success: bool, message: str)
    """
    # Check edit window first
    is_editable, message, _ = check_edit_window(leave_id, user_id)
    if not is_editable:
        return False, message
    
    total_days = calculate_leave_days(from_date, to_date)
    
    with transaction.atomic():
        with connection.cursor() as cursor:
            # Lock the row for update
            cursor.execute("""
                SELECT * FROM attendance_leave_v2 
                WHERE id = %s AND user_id = %s AND status = 'PENDING'
                FOR UPDATE
            """, [leave_id, user_id])
            old_data = dictfetchone(cursor)
            
            if not old_data:
                return False, "Leave request not found or already processed"
            
            # Double-check edit window (race condition protection)
            now = get_ist_now()
            editable_until = old_data['editable_until']
            if isinstance(editable_until, str):
                editable_until = datetime.strptime(editable_until, '%Y-%m-%d %H:%M:%S')
            if editable_until.tzinfo is None:
                editable_until = IST.localize(editable_until)
            
            if now > editable_until:
                return False, f"Edit window expired at {format_ist_datetime(editable_until)}"
            
            # Update the record with date range (DO NOT extend editable_until)
            cursor.execute("""
                UPDATE attendance_leave_v2
                SET leave_date = %s, from_date = %s, to_date = %s, total_days = %s, 
                    leave_type = %s, notes = %s, updated_at = %s
                WHERE id = %s AND user_id = %s AND status = 'PENDING'
            """, [
                from_date, from_date, to_date, total_days, leave_type, notes,
                now.strftime('%Y-%m-%d %H:%M:%S'),
                leave_id, user_id
            ])
            
            if cursor.rowcount == 0:
                return False, "Update failed - record may have been modified"
            
            # Get updated record for audit
            cursor.execute("SELECT * FROM attendance_leave_v2 WHERE id = %s", [leave_id])
            new_data = dictfetchone(cursor)
            
            # Insert audit record
            insert_audit(
                cursor, leave_id, 'EDITED', user_id, 'USER',
                old_data=old_data, new_data=new_data,
                ip_address=ip_address, user_agent=user_agent
            )
            
            return True, "Leave updated successfully"


def cancel_leave_user(leave_id, user_id, reason=None, ip_address=None, user_agent=None):
    """
    Cancel leave request (user) - only within edit window or if PENDING
    Returns: (success: bool, message: str)
    """
    with transaction.atomic():
        with connection.cursor() as cursor:
            # Lock the row
            cursor.execute("""
                SELECT * FROM attendance_leave_v2 
                WHERE id = %s AND user_id = %s
                FOR UPDATE
            """, [leave_id, user_id])
            old_data = dictfetchone(cursor)
            
            if not old_data:
                return False, "Leave request not found"
            
            if old_data['status'] != 'PENDING':
                return False, f"Cannot cancel - status is {old_data['status']}"
            
            now = get_ist_now()
            
            # Update status to CANCELLED
            cursor.execute("""
                UPDATE attendance_leave_v2
                SET status = 'CANCELLED', is_editable = FALSE, updated_at = %s
                WHERE id = %s AND user_id = %s AND status = 'PENDING'
            """, [now.strftime('%Y-%m-%d %H:%M:%S'), leave_id, user_id])
            
            if cursor.rowcount == 0:
                return False, "Cancel failed"
            
            # Get updated record
            cursor.execute("SELECT * FROM attendance_leave_v2 WHERE id = %s", [leave_id])
            new_data = dictfetchone(cursor)
            
            # Insert audit
            insert_audit(
                cursor, leave_id, 'CANCELLED', user_id, 'USER',
                old_data=old_data, new_data=new_data, reason=reason,
                ip_address=ip_address, user_agent=user_agent
            )
            
            return True, "Leave cancelled successfully"


def get_leaves_by_month_user(user_id, year, month):
    """Get all leave records for a user in a specific month"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM vw_leave_details
            WHERE user_id = %s 
            AND YEAR(leave_date) = %s 
            AND MONTH(leave_date) = %s
            ORDER BY leave_date DESC, created_at DESC
        """, [user_id, year, month])
        return dictfetchall(cursor)


def get_leave_stats_user(user_id, year, month):
    """Get leave statistics for a user"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'APPROVED' THEN 1 ELSE 0 END) as approved,
                SUM(CASE WHEN status = 'REJECTED' THEN 1 ELSE 0 END) as rejected,
                SUM(CASE WHEN status = 'PENDING' THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN status = 'CANCELLED' THEN 1 ELSE 0 END) as cancelled
            FROM attendance_leave_v2
            WHERE user_id = %s AND YEAR(leave_date) = %s AND MONTH(leave_date) = %s
        """, [user_id, year, month])
        row = dictfetchone(cursor)
        return {k: int(v or 0) for k, v in row.items()} if row else {
            'total': 0, 'approved': 0, 'rejected': 0, 'pending': 0, 'cancelled': 0
        }


# ============================================
# LEAVE CRUD OPERATIONS - ADMIN
# ============================================

def get_all_leaves_by_month_admin(year, month, status_filter=None, user_filter=None):
    """Get all leave records for admin view"""
    with connection.cursor() as cursor:
        query = """
            SELECT * FROM vw_leave_details
            WHERE YEAR(leave_date) = %s AND MONTH(leave_date) = %s
        """
        params = [year, month]
        
        if status_filter:
            query += " AND status = %s"
            params.append(status_filter)
        
        if user_filter:
            query += " AND user_id = %s"
            params.append(user_filter)
        
        query += " ORDER BY leave_date DESC, created_at DESC"
        
        cursor.execute(query, params)
        return dictfetchall(cursor)


def get_leave_stats_admin(year, month):
    """Get leave statistics for admin dashboard"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'APPROVED' THEN 1 ELSE 0 END) as approved,
                SUM(CASE WHEN status = 'REJECTED' THEN 1 ELSE 0 END) as rejected,
                SUM(CASE WHEN status = 'PENDING' THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN status = 'CANCELLED' THEN 1 ELSE 0 END) as cancelled
            FROM attendance_leave_v2
            WHERE YEAR(leave_date) = %s AND MONTH(leave_date) = %s
        """, [year, month])
        row = dictfetchone(cursor)
        return {k: int(v or 0) for k, v in row.items()} if row else {
            'total': 0, 'approved': 0, 'rejected': 0, 'pending': 0, 'cancelled': 0
        }


def approve_leave_admin(leave_id, admin_id, approval_notes=None, ip_address=None, user_agent=None):
    """
    Approve leave request (admin)
    Returns: (success: bool, message: str, leave_data: dict)
    """
    now = get_ist_now()
    
    with transaction.atomic():
        with connection.cursor() as cursor:
            # Lock and get current record
            cursor.execute("""
                SELECT * FROM attendance_leave_v2 
                WHERE id = %s
                FOR UPDATE
            """, [leave_id])
            old_data = dictfetchone(cursor)
            
            if not old_data:
                return False, "Leave request not found", None
            
            if old_data['status'] != 'PENDING':
                return False, f"Cannot approve - status is already {old_data['status']}", None
            
            # Update to APPROVED
            cursor.execute("""
                UPDATE attendance_leave_v2
                SET status = 'APPROVED', is_editable = FALSE,
                    approved_by = %s, approved_at = %s, approval_notes = %s,
                    updated_at = %s
                WHERE id = %s AND status = 'PENDING'
            """, [
                admin_id,
                now.strftime('%Y-%m-%d %H:%M:%S'),
                approval_notes,
                now.strftime('%Y-%m-%d %H:%M:%S'),
                leave_id
            ])
            
            if cursor.rowcount == 0:
                return False, "Approval failed - record may have been modified", None
            
            # Get updated record with user details
            cursor.execute("SELECT * FROM vw_leave_details WHERE id = %s", [leave_id])
            new_data = dictfetchone(cursor)
            
            # Insert audit
            insert_audit(
                cursor, leave_id, 'APPROVED', admin_id, 'ADMIN',
                old_data=old_data, new_data=new_data,
                ip_address=ip_address, user_agent=user_agent
            )
            
            return True, "Leave approved successfully", new_data


def reject_leave_admin(leave_id, admin_id, reason, approval_notes=None, ip_address=None, user_agent=None):
    """
    Reject leave request (admin)
    Returns: (success: bool, message: str, leave_data: dict)
    """
    now = get_ist_now()
    
    with transaction.atomic():
        with connection.cursor() as cursor:
            # Lock and get current record
            cursor.execute("""
                SELECT * FROM attendance_leave_v2 
                WHERE id = %s
                FOR UPDATE
            """, [leave_id])
            old_data = dictfetchone(cursor)
            
            if not old_data:
                return False, "Leave request not found", None
            
            if old_data['status'] != 'PENDING':
                return False, f"Cannot reject - status is already {old_data['status']}", None
            
            # Update to REJECTED
            cursor.execute("""
                UPDATE attendance_leave_v2
                SET status = 'REJECTED', is_editable = FALSE,
                    approved_by = %s, approved_at = %s, approval_notes = %s,
                    updated_at = %s
                WHERE id = %s AND status = 'PENDING'
            """, [
                admin_id,
                now.strftime('%Y-%m-%d %H:%M:%S'),
                approval_notes or reason,
                now.strftime('%Y-%m-%d %H:%M:%S'),
                leave_id
            ])
            
            if cursor.rowcount == 0:
                return False, "Rejection failed - record may have been modified", None
            
            # Get updated record with user details
            cursor.execute("SELECT * FROM vw_leave_details WHERE id = %s", [leave_id])
            new_data = dictfetchone(cursor)
            
            # Insert audit with reason
            insert_audit(
                cursor, leave_id, 'REJECTED', admin_id, 'ADMIN',
                old_data=old_data, new_data=new_data, reason=reason,
                ip_address=ip_address, user_agent=user_agent
            )
            
            return True, "Leave rejected successfully", new_data


def update_leave_admin(leave_id, admin_id, leave_date, leave_type, notes=None, ip_address=None, user_agent=None):
    """
    Update leave request (admin) - can edit anytime
    Returns: (success: bool, message: str)
    """
    now = get_ist_now()
    
    with transaction.atomic():
        with connection.cursor() as cursor:
            # Lock and get current record
            cursor.execute("""
                SELECT * FROM attendance_leave_v2 
                WHERE id = %s
                FOR UPDATE
            """, [leave_id])
            old_data = dictfetchone(cursor)
            
            if not old_data:
                return False, "Leave request not found"
            
            # Update the record
            cursor.execute("""
                UPDATE attendance_leave_v2
                SET leave_date = %s, leave_type = %s, notes = %s, updated_at = %s
                WHERE id = %s
            """, [
                leave_date, leave_type, notes,
                now.strftime('%Y-%m-%d %H:%M:%S'),
                leave_id
            ])
            
            # Get updated record
            cursor.execute("SELECT * FROM attendance_leave_v2 WHERE id = %s", [leave_id])
            new_data = dictfetchone(cursor)
            
            # Insert audit
            insert_audit(
                cursor, leave_id, 'EDITED', admin_id, 'ADMIN',
                old_data=old_data, new_data=new_data,
                ip_address=ip_address, user_agent=user_agent
            )
            
            return True, "Leave updated successfully"


def delete_leave_admin(leave_id, admin_id, reason=None, ip_address=None, user_agent=None):
    """
    Delete leave request (admin) - soft delete by setting status to CANCELLED
    Returns: (success: bool, message: str)
    """
    now = get_ist_now()
    
    with transaction.atomic():
        with connection.cursor() as cursor:
            # Get current record for audit
            cursor.execute("SELECT * FROM attendance_leave_v2 WHERE id = %s", [leave_id])
            old_data = dictfetchone(cursor)
            
            if not old_data:
                return False, "Leave request not found"
            
            # Soft delete - set status to CANCELLED
            cursor.execute("""
                UPDATE attendance_leave_v2
                SET status = 'CANCELLED', is_editable = FALSE, updated_at = %s
                WHERE id = %s
            """, [now.strftime('%Y-%m-%d %H:%M:%S'), leave_id])
            
            # Get updated record
            cursor.execute("SELECT * FROM attendance_leave_v2 WHERE id = %s", [leave_id])
            new_data = dictfetchone(cursor)
            
            # Insert audit
            insert_audit(
                cursor, leave_id, 'DELETED', admin_id, 'ADMIN',
                old_data=old_data, new_data=new_data, reason=reason,
                ip_address=ip_address, user_agent=user_agent
            )
            
            return True, "Leave deleted successfully"


def get_recent_leaves_admin(limit=10):
    """Get recent leave requests for admin dashboard"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM vw_leave_details
            ORDER BY created_at DESC
            LIMIT %s
        """, [limit])
        return dictfetchall(cursor)


def get_pending_leaves_count():
    """Get count of pending leave requests"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM attendance_leave_v2 WHERE status = 'PENDING'")
        return cursor.fetchone()[0]


def get_all_users_for_filter():
    """Get all users for filter dropdown"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT u.ID, u.EMP_ID, u.EMP_NAME
            FROM users_master u
            INNER JOIN attendance_leave_v2 l ON u.ID = l.user_id
            ORDER BY u.EMP_NAME
        """)
        return dictfetchall(cursor)


# ============================================
# EMAIL TRACKING
# ============================================

def mark_email_sent_admin(leave_id):
    """Mark that admin notification email was sent"""
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE attendance_leave_v2 SET email_sent_admin = TRUE WHERE id = %s
        """, [leave_id])


def mark_email_sent_user(leave_id):
    """Mark that user notification email was sent"""
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE attendance_leave_v2 SET email_sent_user = TRUE WHERE id = %s
        """, [leave_id])
