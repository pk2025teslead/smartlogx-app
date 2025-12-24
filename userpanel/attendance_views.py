"""
SmartLogX Attendance Management Views
Leave, Comp-Off, WFH Management with Raw SQL
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages
from django.db import connection
from datetime import datetime, date, timedelta
import pytz
import json
import logging

from .views import user_login_required, get_current_user
from . import attendance_models as models
from .notification_emails import (
    send_leave_request_notification,
    send_wfh_request_notification,
    send_compoff_request_notification
)

logger = logging.getLogger(__name__)

IST = pytz.timezone('Asia/Kolkata')


def get_current_ist_time():
    """Get current time in IST"""
    return datetime.now(IST)


# ============================================
# ATTENDANCE DASHBOARD
# ============================================

@user_login_required
def attendance_dashboard(request):
    """Attendance management dashboard"""
    user = request.current_user
    current_date = get_current_ist_time()
    year = current_date.year
    month = current_date.month
    
    # Get stats for all modules
    leave_stats = models.get_leave_stats(user['id'], year, month)
    compoff_stats = models.get_compoff_stats(user['id'], year, month)
    wfh_stats = models.get_wfh_stats(user['id'], year, month)
    
    context = {
        'user': user,
        'current_date': current_date,
        'leave_stats': leave_stats,
        'compoff_stats': compoff_stats,
        'wfh_stats': wfh_stats,
        'month_name': current_date.strftime('%B'),
        'year': year,
    }
    
    return render(request, 'userpanel/attendance_dashboard.html', context)


# ============================================
# LEAVE MANAGEMENT VIEWS
# ============================================

@user_login_required
def leave_list(request):
    """Leave list page with month-wise view"""
    user = request.current_user
    current_date = get_current_ist_time()
    
    year = int(request.GET.get('year', current_date.year))
    month = int(request.GET.get('month', current_date.month))
    
    leaves = models.get_leaves_by_month(user['id'], year, month)
    stats = models.get_leave_stats(user['id'], year, month)
    
    # Get saved column order
    column_order = models.get_column_order(user['id'], 'leave')
    
    context = {
        'user': user,
        'leaves': leaves,
        'stats': stats,
        'year': year,
        'month': month,
        'month_name': date(year, month, 1).strftime('%B'),
        'current_date': current_date.strftime('%Y-%m-%d'),
        'is_current_month': year == current_date.year and month == current_date.month,
        'column_order': json.dumps(column_order) if column_order else 'null',
        'leave_types': ['Planned', 'Casual', 'Emergency', 'Sick'],
    }
    
    return render(request, 'userpanel/attendance_leave.html', context)


@user_login_required
def get_leave_detail(request, leave_id):
    """Get leave details (AJAX)"""
    user = request.current_user
    leave = models.get_leave_by_id(leave_id, user['id'])
    
    if not leave:
        return JsonResponse({'success': False, 'error': 'Leave not found'}, status=404)
    
    leave_data = {
        'id': leave['ID'],
        'leave_date': leave['LEAVE_DATE'].strftime('%Y-%m-%d') if leave['LEAVE_DATE'] else '',
        'leave_date_display': leave['LEAVE_DATE'].strftime('%d %B %Y') if leave['LEAVE_DATE'] else '',
        'leave_type': leave['LEAVE_TYPE'],
        'notes': leave['NOTES'] or '',
        'is_approved': leave['IS_APPROVED'],
        'status': 'Approved' if leave['IS_APPROVED'] == 1 else ('Rejected' if leave['IS_APPROVED'] == 0 else 'Pending'),
        'requested_at': leave['REQUESTED_AT'].strftime('%d %B %Y, %I:%M %p') if leave['REQUESTED_AT'] else '',
        'approved_at': leave['APPROVED_AT'].strftime('%d %B %Y, %I:%M %p') if leave['APPROVED_AT'] else '',
        'approval_notes': leave['APPROVAL_NOTES'] or '',
    }
    
    return JsonResponse({'success': True, 'leave': leave_data})


@user_login_required
@require_POST
def save_leave(request):
    """Save new or update leave (AJAX)"""
    user = request.current_user
    
    try:
        data = json.loads(request.body)
        leave_id = data.get('id')
        leave_date = data.get('leave_date', '').strip()
        leave_type = data.get('leave_type', '').strip()
        notes = data.get('notes', '').strip()
        
        # Validation
        errors = []
        if not leave_date:
            errors.append('Leave date is required')
        if not leave_type:
            errors.append('Leave type is required')
        if leave_type not in ['Planned', 'Casual', 'Emergency', 'Sick']:
            errors.append('Invalid leave type')
        
        if errors:
            return JsonResponse({'success': False, 'errors': errors})
        
        if leave_id:
            # Update existing
            result = models.update_leave(leave_id, user['id'], leave_date, leave_type, notes)
            if result == 0:
                return JsonResponse({'success': False, 'error': 'Cannot update approved/rejected leave'})
            message = 'Leave updated successfully'
        else:
            # Create new
            leave_id = models.create_leave(user['id'], leave_date, leave_type, notes)
            message = 'Leave request submitted successfully'
            
            # Send email notification to admin
            try:
                # Format date for display
                formatted_date = datetime.strptime(leave_date, '%Y-%m-%d').strftime('%d %B %Y')
                
                email_success, email_msg = send_leave_request_notification(
                    user_name=user['emp_name'],
                    emp_id=user['emp_id'],
                    leave_date=formatted_date,
                    leave_type=leave_type,
                    notes=notes
                )
                
                if not email_success:
                    logger.warning(f"Leave notification email failed: {email_msg}")
            except Exception as e:
                logger.error(f"Error sending leave notification: {str(e)}")
        
        return JsonResponse({'success': True, 'message': message, 'id': leave_id})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@user_login_required
@require_POST
def delete_leave(request, leave_id):
    """Delete leave request (AJAX)"""
    user = request.current_user
    
    try:
        result = models.delete_leave(leave_id, user['id'])
        if result == 0:
            return JsonResponse({'success': False, 'error': 'Cannot delete approved/rejected leave'})
        return JsonResponse({'success': True, 'message': 'Leave deleted successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ============================================
# COMP-OFF MANAGEMENT VIEWS
# ============================================

@user_login_required
def compoff_list(request):
    """Comp-off list page with month-wise view"""
    user = request.current_user
    current_date = get_current_ist_time()
    
    year = int(request.GET.get('year', current_date.year))
    month = int(request.GET.get('month', current_date.month))
    
    compoffs = models.get_compoffs_by_month(user['id'], year, month)
    stats = models.get_compoff_stats(user['id'], year, month)
    column_order = models.get_column_order(user['id'], 'compoff')
    
    # Generate next 30 days for comp-off date dropdown
    compoff_dates = []
    for i in range(1, 31):
        d = current_date.date() + timedelta(days=i)
        compoff_dates.append({
            'value': d.strftime('%Y-%m-%d'),
            'display': d.strftime('%d %B %Y (%A)')
        })
    
    context = {
        'user': user,
        'compoffs': compoffs,
        'stats': stats,
        'year': year,
        'month': month,
        'month_name': date(year, month, 1).strftime('%B'),
        'current_date': current_date.strftime('%Y-%m-%d'),
        'is_current_month': year == current_date.year and month == current_date.month,
        'column_order': json.dumps(column_order) if column_order else 'null',
        'compoff_dates': compoff_dates,
    }
    
    return render(request, 'userpanel/attendance_compoff.html', context)


@user_login_required
def get_compoff_detail(request, compoff_id):
    """Get comp-off details (AJAX)"""
    user = request.current_user
    compoff = models.get_compoff_by_id(compoff_id, user['id'])
    
    if not compoff:
        return JsonResponse({'success': False, 'error': 'Comp-off not found'}, status=404)
    
    compoff_data = {
        'id': compoff['ID'],
        'sunday_date': compoff['SUNDAY_DATE'].strftime('%Y-%m-%d') if compoff['SUNDAY_DATE'] else '',
        'sunday_date_display': compoff['SUNDAY_DATE'].strftime('%d %B %Y') if compoff['SUNDAY_DATE'] else '',
        'work_purpose': compoff['WORK_PURPOSE'],
        'compoff_date': compoff['COMPOFF_DATE'].strftime('%Y-%m-%d') if compoff['COMPOFF_DATE'] else '',
        'compoff_date_display': compoff['COMPOFF_DATE'].strftime('%d %B %Y') if compoff['COMPOFF_DATE'] else 'No Comp-Off',
        'no_compoff': compoff['NO_COMPOFF'],
        'notes': compoff['NOTES'] or '',
        'is_approved': compoff['IS_APPROVED'],
        'status': 'Approved' if compoff['IS_APPROVED'] == 1 else ('Rejected' if compoff['IS_APPROVED'] == 0 else 'Pending'),
        'requested_at': compoff['REQUESTED_AT'].strftime('%d %B %Y, %I:%M %p') if compoff['REQUESTED_AT'] else '',
    }
    
    return JsonResponse({'success': True, 'compoff': compoff_data})


@user_login_required
@require_POST
def save_compoff(request):
    """Save new or update comp-off (AJAX)"""
    user = request.current_user
    
    try:
        data = json.loads(request.body)
        compoff_id = data.get('id')
        sunday_date = data.get('sunday_date', '').strip()
        work_purpose = data.get('work_purpose', '').strip()
        compoff_date = data.get('compoff_date', '').strip() or None
        no_compoff = data.get('no_compoff', False)
        notes = data.get('notes', '').strip()
        
        # Validation
        errors = []
        if not sunday_date:
            errors.append('Sunday date is required')
        else:
            # Verify it's a Sunday
            try:
                sd = datetime.strptime(sunday_date, '%Y-%m-%d').date()
                if sd.weekday() != 6:  # 6 = Sunday
                    errors.append('Selected date must be a Sunday')
            except:
                errors.append('Invalid date format')
        
        if not work_purpose:
            errors.append('Work purpose is required')
        
        if not no_compoff and not compoff_date:
            errors.append('Please select a comp-off date or choose "No Comp-Off"')
        
        if errors:
            return JsonResponse({'success': False, 'errors': errors})
        
        if no_compoff:
            compoff_date = None
        
        if compoff_id:
            result = models.update_compoff(compoff_id, user['id'], sunday_date, work_purpose, compoff_date, no_compoff, notes)
            if result == 0:
                return JsonResponse({'success': False, 'error': 'Cannot update approved/rejected request'})
            message = 'Comp-off updated successfully'
        else:
            compoff_id = models.create_compoff(user['id'], sunday_date, work_purpose, compoff_date, no_compoff, notes)
            message = 'Comp-off request submitted successfully'
            
            # Send email notification to admin
            try:
                # Format dates for display
                formatted_sunday = datetime.strptime(sunday_date, '%Y-%m-%d').strftime('%d %B %Y')
                formatted_compoff = None
                if compoff_date:
                    formatted_compoff = datetime.strptime(compoff_date, '%Y-%m-%d').strftime('%d %B %Y')
                
                email_success, email_msg = send_compoff_request_notification(
                    user_name=user['emp_name'],
                    emp_id=user['emp_id'],
                    sunday_date=formatted_sunday,
                    work_purpose=work_purpose,
                    compoff_date=formatted_compoff,
                    notes=notes
                )
                
                if not email_success:
                    logger.warning(f"Comp-off notification email failed: {email_msg}")
            except Exception as e:
                logger.error(f"Error sending comp-off notification: {str(e)}")
        
        return JsonResponse({'success': True, 'message': message, 'id': compoff_id})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@user_login_required
@require_POST
def delete_compoff(request, compoff_id):
    """Delete comp-off request (AJAX)"""
    user = request.current_user
    
    try:
        result = models.delete_compoff(compoff_id, user['id'])
        if result == 0:
            return JsonResponse({'success': False, 'error': 'Cannot delete approved/rejected request'})
        return JsonResponse({'success': True, 'message': 'Comp-off deleted successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ============================================
# WFH MANAGEMENT VIEWS
# ============================================

@user_login_required
def wfh_list(request):
    """WFH list page with month-wise view"""
    user = request.current_user
    current_date = get_current_ist_time()
    
    year = int(request.GET.get('year', current_date.year))
    month = int(request.GET.get('month', current_date.month))
    
    wfh_records = models.get_wfh_by_month(user['id'], year, month)
    stats = models.get_wfh_stats(user['id'], year, month)
    column_order = models.get_column_order(user['id'], 'wfh')
    
    context = {
        'user': user,
        'wfh_records': wfh_records,
        'stats': stats,
        'year': year,
        'month': month,
        'month_name': date(year, month, 1).strftime('%B'),
        'current_date': current_date.strftime('%Y-%m-%d'),
        'is_current_month': year == current_date.year and month == current_date.month,
        'column_order': json.dumps(column_order) if column_order else 'null',
    }
    
    return render(request, 'userpanel/attendance_wfh.html', context)


@user_login_required
def get_wfh_detail(request, wfh_id):
    """Get WFH details (AJAX)"""
    user = request.current_user
    wfh = models.get_wfh_by_id(wfh_id, user['id'])
    
    if not wfh:
        return JsonResponse({'success': False, 'error': 'WFH record not found'}, status=404)
    
    wfh_data = {
        'id': wfh['ID'],
        'wfh_date': wfh['WFH_DATE'].strftime('%Y-%m-%d') if wfh['WFH_DATE'] else '',
        'wfh_date_display': wfh['WFH_DATE'].strftime('%d %B %Y') if wfh['WFH_DATE'] else '',
        'reason': wfh['REASON'],
        'notes': wfh['NOTES'] or '',
        'is_approved': wfh['IS_APPROVED'],
        'status': 'Approved' if wfh['IS_APPROVED'] == 1 else ('Rejected' if wfh['IS_APPROVED'] == 0 else 'Pending'),
        'requested_at': wfh['REQUESTED_AT'].strftime('%d %B %Y, %I:%M %p') if wfh['REQUESTED_AT'] else '',
    }
    
    return JsonResponse({'success': True, 'wfh': wfh_data})


@user_login_required
@require_POST
def save_wfh(request):
    """Save new or update WFH (AJAX)"""
    user = request.current_user
    
    try:
        data = json.loads(request.body)
        wfh_id = data.get('id')
        wfh_date = data.get('wfh_date', '').strip()
        reason = data.get('reason', '').strip()
        notes = data.get('notes', '').strip()
        
        # Validation
        errors = []
        if not wfh_date:
            errors.append('WFH date is required')
        if not reason:
            errors.append('Reason is required')
        
        if errors:
            return JsonResponse({'success': False, 'errors': errors})
        
        if wfh_id:
            result = models.update_wfh(wfh_id, user['id'], wfh_date, reason, notes)
            if result == 0:
                return JsonResponse({'success': False, 'error': 'Cannot update approved/rejected request'})
            message = 'WFH updated successfully'
        else:
            wfh_id = models.create_wfh(user['id'], wfh_date, reason, notes)
            message = 'WFH request submitted successfully'
            
            # Send email notification to admin
            try:
                # Format date for display
                formatted_date = datetime.strptime(wfh_date, '%Y-%m-%d').strftime('%d %B %Y')
                
                email_success, email_msg = send_wfh_request_notification(
                    user_name=user['emp_name'],
                    emp_id=user['emp_id'],
                    wfh_date=formatted_date,
                    reason=reason,
                    notes=notes
                )
                
                if not email_success:
                    logger.warning(f"WFH notification email failed: {email_msg}")
            except Exception as e:
                logger.error(f"Error sending WFH notification: {str(e)}")
        
        return JsonResponse({'success': True, 'message': message, 'id': wfh_id})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@user_login_required
@require_POST
def delete_wfh(request, wfh_id):
    """Delete WFH request (AJAX)"""
    user = request.current_user
    
    try:
        result = models.delete_wfh(wfh_id, user['id'])
        if result == 0:
            return JsonResponse({'success': False, 'error': 'Cannot delete approved/rejected request'})
        return JsonResponse({'success': True, 'message': 'WFH deleted successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ============================================
# COLUMN ORDER SAVE (AJAX)
# ============================================

@user_login_required
@require_POST
def save_column_order(request):
    """Save column order preference (AJAX)"""
    user = request.current_user
    
    try:
        data = json.loads(request.body)
        table_name = data.get('table_name', '').strip()
        column_order = data.get('column_order', [])
        
        if not table_name or not column_order:
            return JsonResponse({'success': False, 'error': 'Invalid data'})
        
        models.save_column_order(user['id'], table_name, column_order)
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
