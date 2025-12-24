"""
SmartLogX Admin Panel - Attendance & Log Management Views
Raw SQL Operations with Admin Permission Checks
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from datetime import datetime, date
import json
import os

from . import attendance_models as models


def is_admin(user):
    """Check if user is admin/staff"""
    return user.is_staff


def get_admin_id(request):
    """Get admin user ID from users_master or auth_user"""
    # For now, return the auth_user id; adjust if using users_master for admins
    return request.user.id


# ============================================
# ADMIN DASHBOARD
# ============================================

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard with statistics and recent entries"""
    stats = models.get_dashboard_stats()
    
    # Get recent entries
    recent_leaves = models.get_recent_leaves(5)
    recent_compoffs = models.get_recent_compoffs(5)
    recent_wfh = models.get_recent_wfh(5)
    recent_logs = models.get_recent_logs(5)
    
    current_date = datetime.now()
    
    context = {
        'stats': stats,
        'recent_leaves': recent_leaves,
        'recent_compoffs': recent_compoffs,
        'recent_wfh': recent_wfh,
        'recent_logs': recent_logs,
        'current_month': current_date.strftime('%B %Y'),
        'stats_json': json.dumps(stats),
    }
    
    return render(request, 'adminpanel/dashboard_admin.html', context)


# ============================================
# LEAVE MANAGEMENT - Admin Views
# ============================================

@login_required
@user_passes_test(is_admin)
def leave_list_admin(request):
    """Leave list page for admin"""
    current_date = datetime.now()
    year = int(request.GET.get('year', current_date.year))
    month = int(request.GET.get('month', current_date.month))
    
    leaves = models.get_all_leaves_by_month(year, month)
    stats = models.get_leave_stats(year, month)
    
    context = {
        'leaves': leaves,
        'stats': stats,
        'year': year,
        'month': month,
        'month_name': date(year, month, 1).strftime('%B'),
        'is_current_month': year == current_date.year and month == current_date.month,
        'leave_types': ['Planned', 'Casual', 'Emergency', 'Sick'],
    }
    
    return render(request, 'adminpanel/leave_list_admin.html', context)


@login_required
@user_passes_test(is_admin)
def leave_list_json(request):
    """Get leave list as JSON (AJAX)"""
    year = int(request.GET.get('year', datetime.now().year))
    month = int(request.GET.get('month', datetime.now().month))
    
    leaves = models.get_all_leaves_by_month(year, month)
    
    # Format dates for JSON
    for leave in leaves:
        if leave.get('LEAVE_DATE'):
            leave['LEAVE_DATE'] = leave['LEAVE_DATE'].strftime('%Y-%m-%d')
        if leave.get('CREATED_AT'):
            leave['CREATED_AT'] = leave['CREATED_AT'].strftime('%Y-%m-%d %H:%M')
    
    return JsonResponse({'success': True, 'data': leaves})


@login_required
@user_passes_test(is_admin)
def leave_detail_admin(request, leave_id):
    """Get leave detail (AJAX)"""
    leave = models.get_leave_by_id(leave_id)
    
    if not leave:
        return JsonResponse({'success': False, 'error': 'Leave not found'}, status=404)
    
    # Format dates
    leave_data = {
        'id': leave['ID'],
        'user_name': leave['EMP_NAME'],
        'user_id': leave['EMP_ID'],
        'leave_date': leave['LEAVE_DATE'].strftime('%Y-%m-%d') if leave['LEAVE_DATE'] else '',
        'leave_date_display': leave['LEAVE_DATE'].strftime('%d %B %Y') if leave['LEAVE_DATE'] else '',
        'leave_type': leave['LEAVE_TYPE'],
        'notes': leave['NOTES'] or '',
        'is_approved': leave['IS_APPROVED'],
        'status': 'Approved' if leave['IS_APPROVED'] == 1 else ('Rejected' if leave['IS_APPROVED'] == 0 else 'Pending'),
        'approver_name': leave.get('APPROVER_NAME') or '',
        'approval_notes': leave.get('APPROVAL_NOTES') or '',
        'requested_at': leave['REQUESTED_AT'].strftime('%d %B %Y, %I:%M %p') if leave.get('REQUESTED_AT') else '',
        'approved_at': leave['APPROVED_AT'].strftime('%d %B %Y, %I:%M %p') if leave.get('APPROVED_AT') else '',
    }
    
    return JsonResponse({'success': True, 'leave': leave_data})


@login_required
@user_passes_test(is_admin)
@require_POST
def leave_update_admin(request, leave_id):
    """Update leave (AJAX)"""
    try:
        data = json.loads(request.body)
        leave_date = data.get('leave_date')
        leave_type = data.get('leave_type')
        notes = data.get('notes', '')
        
        if not leave_date or not leave_type:
            return JsonResponse({'success': False, 'error': 'Date and type are required'})
        
        result = models.update_leave_admin(leave_id, leave_date, leave_type, notes)
        
        if result:
            return JsonResponse({'success': True, 'message': 'Leave updated successfully'})
        return JsonResponse({'success': False, 'error': 'Update failed'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@user_passes_test(is_admin)
@require_POST
def leave_delete_admin(request, leave_id):
    """Delete leave (AJAX)"""
    try:
        result = models.delete_leave_admin(leave_id)
        if result:
            return JsonResponse({'success': True, 'message': 'Leave deleted successfully'})
        return JsonResponse({'success': False, 'error': 'Delete failed'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@user_passes_test(is_admin)
@require_POST
def leave_approve_admin(request, leave_id):
    """Approve/Reject leave (AJAX)"""
    try:
        data = json.loads(request.body)
        is_approved = data.get('is_approved')  # 1 for approve, 0 for reject
        approval_notes = data.get('approval_notes', '')
        
        admin_id = get_admin_id(request)
        result = models.approve_reject_leave(leave_id, admin_id, is_approved, approval_notes)
        
        if result:
            action = 'approved' if is_approved else 'rejected'
            
            # ============================================
            # EMAIL NOTIFICATION - UNCOMMENT IN PRODUCTION
            # ============================================
            # from django.core.mail import send_mail
            # from django.conf import settings
            # 
            # leave = models.get_leave_by_id(leave_id)
            # user_email = leave.get('USER_EMAIL')
            # 
            # subject = f'Leave Request {action.title()} - SmartLogX'
            # body = f'''
            # Dear {leave.get('EMP_NAME')},
            # 
            # Your leave request for {leave.get('LEAVE_DATE')} has been {action}.
            # 
            # Leave Type: {leave.get('LEAVE_TYPE')}
            # Admin Notes: {approval_notes or 'N/A'}
            # 
            # - SmartLogX Admin
            # '''
            # 
            # try:
            #     send_mail(
            #         subject, body,
            #         settings.EMAIL_HOST_USER,
            #         [user_email],
            #         fail_silently=False
            #     )
            # except Exception as e:
            #     print(f"Email error: {e}")
            # ============================================
            
            return JsonResponse({'success': True, 'message': f'Leave {action} successfully'})
        return JsonResponse({'success': False, 'error': 'Action failed'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ============================================
# COMP-OFF MANAGEMENT - Admin Views
# ============================================

@login_required
@user_passes_test(is_admin)
def compoff_list_admin(request):
    """Comp-off list page for admin"""
    current_date = datetime.now()
    year = int(request.GET.get('year', current_date.year))
    month = int(request.GET.get('month', current_date.month))
    
    compoffs = models.get_all_compoffs_by_month(year, month)
    stats = models.get_compoff_stats(year, month)
    
    context = {
        'compoffs': compoffs,
        'stats': stats,
        'year': year,
        'month': month,
        'month_name': date(year, month, 1).strftime('%B'),
        'is_current_month': year == current_date.year and month == current_date.month,
    }
    
    return render(request, 'adminpanel/compoff_list_admin.html', context)


@login_required
@user_passes_test(is_admin)
def compoff_detail_admin(request, compoff_id):
    """Get comp-off detail (AJAX)"""
    compoff = models.get_compoff_by_id(compoff_id)
    
    if not compoff:
        return JsonResponse({'success': False, 'error': 'Comp-off not found'}, status=404)
    
    compoff_data = {
        'id': compoff['ID'],
        'user_name': compoff['EMP_NAME'],
        'user_id': compoff['EMP_ID'],
        'sunday_date': compoff['SUNDAY_DATE'].strftime('%Y-%m-%d') if compoff['SUNDAY_DATE'] else '',
        'sunday_date_display': compoff['SUNDAY_DATE'].strftime('%d %B %Y') if compoff['SUNDAY_DATE'] else '',
        'work_purpose': compoff['WORK_PURPOSE'],
        'compoff_date': compoff['COMPOFF_DATE'].strftime('%Y-%m-%d') if compoff['COMPOFF_DATE'] else '',
        'compoff_date_display': compoff['COMPOFF_DATE'].strftime('%d %B %Y') if compoff['COMPOFF_DATE'] else 'No Comp-Off',
        'no_compoff': compoff['NO_COMPOFF'],
        'notes': compoff['NOTES'] or '',
        'is_approved': compoff['IS_APPROVED'],
        'status': 'Approved' if compoff['IS_APPROVED'] == 1 else ('Rejected' if compoff['IS_APPROVED'] == 0 else 'Pending'),
    }
    
    return JsonResponse({'success': True, 'compoff': compoff_data})


@login_required
@user_passes_test(is_admin)
@require_POST
def compoff_update_admin(request, compoff_id):
    """Update comp-off (AJAX)"""
    try:
        data = json.loads(request.body)
        sunday_date = data.get('sunday_date')
        work_purpose = data.get('work_purpose')
        compoff_date = data.get('compoff_date') or None
        no_compoff = data.get('no_compoff', False)
        notes = data.get('notes', '')
        
        # Validate Sunday
        if sunday_date:
            sd = datetime.strptime(sunday_date, '%Y-%m-%d').date()
            if sd.weekday() != 6:
                return JsonResponse({'success': False, 'error': 'Date must be a Sunday'})
        
        result = models.update_compoff_admin(compoff_id, sunday_date, work_purpose, compoff_date, no_compoff, notes)
        
        if result:
            return JsonResponse({'success': True, 'message': 'Comp-off updated successfully'})
        return JsonResponse({'success': False, 'error': 'Update failed'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@user_passes_test(is_admin)
@require_POST
def compoff_delete_admin(request, compoff_id):
    """Delete comp-off (AJAX)"""
    try:
        result = models.delete_compoff_admin(compoff_id)
        if result:
            return JsonResponse({'success': True, 'message': 'Comp-off deleted successfully'})
        return JsonResponse({'success': False, 'error': 'Delete failed'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@user_passes_test(is_admin)
@require_POST
def compoff_approve_admin(request, compoff_id):
    """Approve/Reject comp-off (AJAX)"""
    try:
        data = json.loads(request.body)
        is_approved = data.get('is_approved')
        approval_notes = data.get('approval_notes', '')
        
        admin_id = get_admin_id(request)
        result = models.approve_reject_compoff(compoff_id, admin_id, is_approved, approval_notes)
        
        if result:
            action = 'approved' if is_approved else 'rejected'
            # EMAIL NOTIFICATION CODE HERE (COMMENTED) - same pattern as leave
            return JsonResponse({'success': True, 'message': f'Comp-off {action} successfully'})
        return JsonResponse({'success': False, 'error': 'Action failed'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ============================================
# WFH MANAGEMENT - Admin Views
# ============================================

@login_required
@user_passes_test(is_admin)
def wfh_list_admin(request):
    """WFH list page for admin"""
    current_date = datetime.now()
    year = int(request.GET.get('year', current_date.year))
    month = int(request.GET.get('month', current_date.month))
    
    wfh_records = models.get_all_wfh_by_month(year, month)
    stats = models.get_wfh_stats(year, month)
    
    context = {
        'wfh_records': wfh_records,
        'stats': stats,
        'year': year,
        'month': month,
        'month_name': date(year, month, 1).strftime('%B'),
        'is_current_month': year == current_date.year and month == current_date.month,
    }
    
    return render(request, 'adminpanel/wfh_list_admin.html', context)


@login_required
@user_passes_test(is_admin)
def wfh_detail_admin(request, wfh_id):
    """Get WFH detail (AJAX)"""
    wfh = models.get_wfh_by_id(wfh_id)
    
    if not wfh:
        return JsonResponse({'success': False, 'error': 'WFH not found'}, status=404)
    
    wfh_data = {
        'id': wfh['ID'],
        'user_name': wfh['EMP_NAME'],
        'user_id': wfh['EMP_ID'],
        'wfh_date': wfh['WFH_DATE'].strftime('%Y-%m-%d') if wfh['WFH_DATE'] else '',
        'wfh_date_display': wfh['WFH_DATE'].strftime('%d %B %Y') if wfh['WFH_DATE'] else '',
        'reason': wfh['REASON'],
        'notes': wfh['NOTES'] or '',
        'is_approved': wfh['IS_APPROVED'],
        'status': 'Approved' if wfh['IS_APPROVED'] == 1 else ('Rejected' if wfh['IS_APPROVED'] == 0 else 'Pending'),
    }
    
    return JsonResponse({'success': True, 'wfh': wfh_data})


@login_required
@user_passes_test(is_admin)
@require_POST
def wfh_update_admin(request, wfh_id):
    """Update WFH (AJAX)"""
    try:
        data = json.loads(request.body)
        wfh_date = data.get('wfh_date')
        reason = data.get('reason')
        notes = data.get('notes', '')
        
        result = models.update_wfh_admin(wfh_id, wfh_date, reason, notes)
        
        if result:
            return JsonResponse({'success': True, 'message': 'WFH updated successfully'})
        return JsonResponse({'success': False, 'error': 'Update failed'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@user_passes_test(is_admin)
@require_POST
def wfh_delete_admin(request, wfh_id):
    """Delete WFH (AJAX)"""
    try:
        result = models.delete_wfh_admin(wfh_id)
        if result:
            return JsonResponse({'success': True, 'message': 'WFH deleted successfully'})
        return JsonResponse({'success': False, 'error': 'Delete failed'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@user_passes_test(is_admin)
@require_POST
def wfh_approve_admin(request, wfh_id):
    """Approve/Reject WFH (AJAX)"""
    try:
        data = json.loads(request.body)
        is_approved = data.get('is_approved')
        approval_notes = data.get('approval_notes', '')
        
        admin_id = get_admin_id(request)
        result = models.approve_reject_wfh(wfh_id, admin_id, is_approved, approval_notes)
        
        if result:
            action = 'approved' if is_approved else 'rejected'
            return JsonResponse({'success': True, 'message': f'WFH {action} successfully'})
        return JsonResponse({'success': False, 'error': 'Action failed'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ============================================
# LOG MANAGEMENT - Admin Views
# ============================================

@login_required
@user_passes_test(is_admin)
def log_list_admin(request):
    """Log list page for admin"""
    current_date = datetime.now()
    year = int(request.GET.get('year', current_date.year))
    month = int(request.GET.get('month', current_date.month))
    
    logs = models.get_all_logs_by_month(year, month)
    stats = models.get_log_stats(year, month)
    
    context = {
        'logs': logs,
        'stats': stats,
        'year': year,
        'month': month,
        'month_name': date(year, month, 1).strftime('%B'),
        'is_current_month': year == current_date.year and month == current_date.month,
    }
    
    return render(request, 'adminpanel/log_list_admin.html', context)


@login_required
@user_passes_test(is_admin)
def log_detail_admin(request, log_id):
    """Get log detail (AJAX)"""
    log = models.get_log_by_id(log_id)
    
    if not log:
        return JsonResponse({'success': False, 'error': 'Log not found'}, status=404)
    
    log_data = {
        'id': log['ID'],
        'user_name': log['EMP_NAME'],
        'user_id': log['EMP_ID'],
        'project_title': log['PROJECT_TITLE'],
        'log_heading': log['LOG_HEADING'],
        'log_details': log['LOG_DETAILS'],
        'log_date': log['LOG_DATE'].strftime('%Y-%m-%d') if log['LOG_DATE'] else '',
        'log_date_display': log['LOG_DATE'].strftime('%d %B %Y') if log['LOG_DATE'] else '',
        'session_type': log['SESSION_TYPE'],
        'approval_required': log['APPROVAL_REQUIRED'],
        'created_at': log['CREATED_AT'].strftime('%d %B %Y, %I:%M %p') if log['CREATED_AT'] else '',
    }
    
    return JsonResponse({'success': True, 'log': log_data})
