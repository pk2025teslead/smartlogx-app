"""
SmartLogX Leave Management Module - Admin Views
Raw SQL with 10-minute edit window and audit trail
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, date
import json
import logging

from . import leave_models as models
from . import leave_emails as emails

logger = logging.getLogger(__name__)


def is_admin(user):
    """Check if user is admin/staff"""
    return user.is_staff


def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def get_user_agent(request):
    """Get user agent string"""
    return request.META.get('HTTP_USER_AGENT', '')[:500]


# ============================================
# ADMIN LEAVE LIST VIEW
# ============================================

@login_required
@user_passes_test(is_admin)
def leave_list_admin_v2(request):
    """Leave list page for admin with enhanced features"""
    current_date = datetime.now()
    year = int(request.GET.get('year', current_date.year))
    month = int(request.GET.get('month', current_date.month))
    status_filter = request.GET.get('status', '')
    user_filter = request.GET.get('user_id', '')
    
    leaves = models.get_all_leaves_by_month_admin(
        year, month,
        status_filter=status_filter if status_filter else None,
        user_filter=int(user_filter) if user_filter else None
    )
    stats = models.get_leave_stats_admin(year, month)
    users = models.get_all_users_for_filter()
    
    # Format dates for display
    for leave in leaves:
        if leave.get('leave_date'):
            leave['leave_date_display'] = leave['leave_date'].strftime('%d %b, %Y')
        if leave.get('created_at'):
            leave['created_at_display'] = leave['created_at'].strftime('%d %b %Y, %I:%M %p')
        if leave.get('editable_until'):
            leave['editable_until_display'] = models.format_ist_datetime(leave['editable_until'])
    
    context = {
        'leaves': leaves,
        'stats': stats,
        'users': users,
        'year': year,
        'month': month,
        'month_name': date(year, month, 1).strftime('%B'),
        'is_current_month': year == current_date.year and month == current_date.month,
        'leave_types': ['PLANNED', 'CASUAL', 'EMERGENCY', 'SICK'],
        'status_options': ['PENDING', 'APPROVED', 'REJECTED', 'CANCELLED'],
        'current_status': status_filter,
        'current_user': user_filter,
    }
    
    return render(request, 'adminpanel/leave_list_admin.html', context)


@login_required
@user_passes_test(is_admin)
def leave_list_json_v2(request):
    """Get leave list as JSON (AJAX)"""
    year = int(request.GET.get('year', datetime.now().year))
    month = int(request.GET.get('month', datetime.now().month))
    status_filter = request.GET.get('status', '')
    user_filter = request.GET.get('user_id', '')
    
    leaves = models.get_all_leaves_by_month_admin(
        year, month,
        status_filter=status_filter if status_filter else None,
        user_filter=int(user_filter) if user_filter else None
    )
    
    # Format for JSON
    for leave in leaves:
        for key, value in leave.items():
            if isinstance(value, (datetime, date)):
                leave[key] = value.isoformat()
    
    return JsonResponse({'success': True, 'data': leaves})


# ============================================
# ADMIN LEAVE DETAIL
# ============================================

@login_required
@user_passes_test(is_admin)
def leave_detail_admin_v2(request, leave_id):
    """Get leave detail with audit trail (AJAX)"""
    leave = models.get_leave_by_id(leave_id)
    
    if not leave:
        return JsonResponse({'success': False, 'error': 'Leave not found'}, status=404)
    
    # Get audit trail
    audit_trail = models.get_audit_trail(leave_id, limit=20)
    
    # Format dates
    leave_data = {
        'id': leave['id'],
        'user_name': leave.get('emp_name', ''),
        'user_id': leave.get('emp_id', ''),
        'user_email': leave.get('user_email', ''),
        'leave_date': leave['leave_date'].strftime('%Y-%m-%d') if leave.get('leave_date') else '',
        'leave_date_display': leave['leave_date'].strftime('%d %B %Y') if leave.get('leave_date') else '',
        'leave_type': leave.get('leave_type', ''),
        'notes': leave.get('notes') or '',
        'status': leave.get('status', 'PENDING'),
        'is_editable': leave.get('is_currently_editable', False),
        'edit_seconds_remaining': leave.get('edit_seconds_remaining', 0),
        'editable_until': models.format_ist_datetime(leave.get('editable_until')),
        'approver_name': leave.get('approver_name') or '',
        'approval_notes': leave.get('approval_notes') or '',
        'created_at': models.format_ist_datetime(leave.get('created_at')),
        'approved_at': models.format_ist_datetime(leave.get('approved_at')),
    }
    
    # Format audit trail
    for audit in audit_trail:
        if audit.get('created_at'):
            audit['created_at'] = models.format_ist_datetime(audit['created_at'])
        if audit.get('old_data') and isinstance(audit['old_data'], str):
            audit['old_data'] = json.loads(audit['old_data'])
        if audit.get('new_data') and isinstance(audit['new_data'], str):
            audit['new_data'] = json.loads(audit['new_data'])
    
    return JsonResponse({
        'success': True,
        'leave': leave_data,
        'audit_trail': audit_trail
    })


# ============================================
# ADMIN APPROVE/REJECT
# ============================================

@login_required
@user_passes_test(is_admin)
@require_POST
def leave_approve_admin_v2(request, leave_id):
    """Approve leave request (AJAX)"""
    try:
        data = json.loads(request.body)
        approval_notes = data.get('approval_notes', '')
        
        admin_id = request.user.id
        ip_address = get_client_ip(request)
        user_agent = get_user_agent(request)
        
        success, message, leave_data = models.approve_leave_admin(
            leave_id, admin_id, approval_notes,
            ip_address=ip_address, user_agent=user_agent
        )
        
        if success and leave_data:
            # Send email notification to user
            try:
                email_success, email_msg = emails.send_leave_approved_notification(leave_data)
                if email_success:
                    models.mark_email_sent_user(leave_id)
                else:
                    logger.warning(f"Approval email failed for leave {leave_id}: {email_msg}")
            except Exception as e:
                logger.error(f"Error sending approval email: {e}")
        
        return JsonResponse({'success': success, 'message': message})
        
    except Exception as e:
        logger.exception(f"Error approving leave {leave_id}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@user_passes_test(is_admin)
@require_POST
def leave_reject_admin_v2(request, leave_id):
    """Reject leave request (AJAX)"""
    try:
        data = json.loads(request.body)
        reason = data.get('reason', '')
        approval_notes = data.get('approval_notes', '')
        
        if not reason:
            return JsonResponse({'success': False, 'error': 'Rejection reason is required'})
        
        admin_id = request.user.id
        ip_address = get_client_ip(request)
        user_agent = get_user_agent(request)
        
        success, message, leave_data = models.reject_leave_admin(
            leave_id, admin_id, reason, approval_notes,
            ip_address=ip_address, user_agent=user_agent
        )
        
        if success and leave_data:
            # Send email notification to user
            try:
                email_success, email_msg = emails.send_leave_rejected_notification(leave_data, reason)
                if email_success:
                    models.mark_email_sent_user(leave_id)
                else:
                    logger.warning(f"Rejection email failed for leave {leave_id}: {email_msg}")
            except Exception as e:
                logger.error(f"Error sending rejection email: {e}")
        
        return JsonResponse({'success': success, 'message': message})
        
    except Exception as e:
        logger.exception(f"Error rejecting leave {leave_id}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ============================================
# ADMIN UPDATE/DELETE
# ============================================

@login_required
@user_passes_test(is_admin)
@require_POST
def leave_update_admin_v2(request, leave_id):
    """Update leave request (admin can edit anytime)"""
    try:
        data = json.loads(request.body)
        leave_date = data.get('leave_date')
        leave_type = data.get('leave_type')
        notes = data.get('notes', '')
        
        if not leave_date or not leave_type:
            return JsonResponse({'success': False, 'error': 'Date and type are required'})
        
        admin_id = request.user.id
        ip_address = get_client_ip(request)
        user_agent = get_user_agent(request)
        
        success, message = models.update_leave_admin(
            leave_id, admin_id, leave_date, leave_type, notes,
            ip_address=ip_address, user_agent=user_agent
        )
        
        return JsonResponse({'success': success, 'message': message})
        
    except Exception as e:
        logger.exception(f"Error updating leave {leave_id}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@user_passes_test(is_admin)
@require_POST
def leave_delete_admin_v2(request, leave_id):
    """Delete (soft) leave request"""
    try:
        data = json.loads(request.body) if request.body else {}
        reason = data.get('reason', 'Deleted by admin')
        
        admin_id = request.user.id
        ip_address = get_client_ip(request)
        user_agent = get_user_agent(request)
        
        success, message = models.delete_leave_admin(
            leave_id, admin_id, reason,
            ip_address=ip_address, user_agent=user_agent
        )
        
        return JsonResponse({'success': success, 'message': message})
        
    except Exception as e:
        logger.exception(f"Error deleting leave {leave_id}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ============================================
# ADMIN AUDIT TRAIL
# ============================================

@login_required
@user_passes_test(is_admin)
def leave_audit_admin(request, leave_id):
    """Get audit trail for a leave request"""
    audit_trail = models.get_audit_trail(leave_id, limit=50)
    
    # Format for display
    for audit in audit_trail:
        if audit.get('created_at'):
            audit['created_at'] = models.format_ist_datetime(audit['created_at'])
        if audit.get('old_data') and isinstance(audit['old_data'], str):
            audit['old_data'] = json.loads(audit['old_data'])
        if audit.get('new_data') and isinstance(audit['new_data'], str):
            audit['new_data'] = json.loads(audit['new_data'])
    
    return JsonResponse({'success': True, 'audit_trail': audit_trail})
