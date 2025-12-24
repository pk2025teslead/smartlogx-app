"""
SmartLogX Leave Management Module - User Views
Raw SQL with 10-minute edit window and audit trail
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from datetime import datetime, date
import json
import logging

from .views import user_login_required, get_current_user
from adminpanel import leave_models as models
from adminpanel import leave_emails as emails

logger = logging.getLogger(__name__)


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
# USER LEAVE LIST VIEW
# ============================================

@user_login_required
def leave_list_user_v2(request):
    """Leave list page for user with edit window timer and date range support"""
    user = request.current_user
    current_date = models.get_ist_now()
    
    year = int(request.GET.get('year', current_date.year))
    month = int(request.GET.get('month', current_date.month))
    
    leaves = models.get_leaves_by_month_user(user['id'], year, month)
    stats = models.get_leave_stats_user(user['id'], year, month)
    
    # Add edit window info and format dates for each leave
    for leave in leaves:
        # Format date display based on date range
        from_date = leave.get('from_date') or leave.get('leave_date')
        to_date = leave.get('to_date') or leave.get('leave_date')
        total_days = leave.get('total_days', 1)
        
        if from_date and to_date:
            if from_date == to_date:
                leave['leave_date_display'] = from_date.strftime('%d %b, %Y')
            else:
                leave['leave_date_display'] = f"{from_date.strftime('%d %b')} - {to_date.strftime('%d %b, %Y')}"
        elif leave.get('leave_date'):
            leave['leave_date_display'] = leave['leave_date'].strftime('%d %b, %Y')
        
        leave['total_days'] = total_days
        leave['days_badge'] = f"{total_days} day{'s' if total_days > 1 else ''}"
        
        if leave.get('created_at'):
            leave['created_at_display'] = leave['created_at'].strftime('%d %b %Y, %I:%M %p')
        if leave.get('editable_until'):
            leave['editable_until_display'] = models.format_ist_datetime(leave['editable_until'])
        # Real-time editability check
        leave['can_edit'] = leave.get('is_currently_editable', False)
        leave['seconds_remaining'] = max(0, leave.get('edit_seconds_remaining', 0))
    
    context = {
        'user': user,
        'leaves': leaves,
        'stats': stats,
        'year': year,
        'month': month,
        'month_name': date(year, month, 1).strftime('%B'),
        'current_date': current_date.strftime('%Y-%m-%d'),
        'is_current_month': year == current_date.year and month == current_date.month,
        'leave_types': ['PLANNED', 'CASUAL', 'EMERGENCY', 'SICK'],
        'edit_window_minutes': models.EDIT_WINDOW_MINUTES,
    }
    
    return render(request, 'userpanel/attendance_leave.html', context)


# ============================================
# USER LEAVE DETAIL
# ============================================

@user_login_required
def leave_detail_user_v2(request, leave_id):
    """Get leave detail for user (AJAX)"""
    user = request.current_user
    leave = models.get_leave_by_id(leave_id, user['id'])
    
    if not leave:
        return JsonResponse({'success': False, 'error': 'Leave not found'}, status=404)
    
    # Check edit window
    is_editable, edit_message, seconds_remaining = models.check_edit_window(leave_id, user['id'])
    
    # Format date display based on date range
    from_date = leave.get('from_date') or leave.get('leave_date')
    to_date = leave.get('to_date') or leave.get('leave_date')
    total_days = leave.get('total_days', 1)
    
    if from_date == to_date:
        date_display = from_date.strftime('%d %B %Y') if from_date else ''
    else:
        date_display = f"{from_date.strftime('%d %b')} - {to_date.strftime('%d %b %Y')}" if from_date and to_date else ''
    
    leave_data = {
        'id': leave['id'],
        'from_date': from_date.strftime('%Y-%m-%d') if from_date else '',
        'to_date': to_date.strftime('%Y-%m-%d') if to_date else '',
        'total_days': total_days,
        'leave_date_display': date_display,
        'leave_type': leave.get('leave_type', ''),
        'notes': leave.get('notes') or '',
        'status': leave.get('status', 'PENDING'),
        'is_editable': is_editable,
        'edit_message': edit_message,
        'seconds_remaining': seconds_remaining,
        'editable_until': models.format_ist_datetime(leave.get('editable_until')),
        'approver_name': leave.get('approver_name') or '',
        'approval_notes': leave.get('approval_notes') or '',
        'created_at': models.format_ist_datetime(leave.get('created_at')),
        'approved_at': models.format_ist_datetime(leave.get('approved_at')),
    }
    
    return JsonResponse({'success': True, 'leave': leave_data})


# ============================================
# USER CREATE LEAVE
# ============================================

@user_login_required
@require_POST
def leave_create_user_v2(request):
    """Create new leave request with date range (AJAX)"""
    user = request.current_user
    
    try:
        data = json.loads(request.body)
        from_date = data.get('from_date', '').strip()
        to_date = data.get('to_date', '').strip()
        leave_type = data.get('leave_type', '').strip().upper()
        notes = data.get('notes', '').strip()
        
        # Validation
        errors = []
        today = models.get_ist_now().date()
        
        if not from_date:
            errors.append('From date is required')
        else:
            try:
                parsed_from = datetime.strptime(from_date, '%Y-%m-%d').date()
                if parsed_from < today:
                    errors.append('From date cannot be in the past')
            except ValueError:
                errors.append('Invalid from date format')
        
        if not to_date:
            errors.append('To date is required')
        else:
            try:
                parsed_to = datetime.strptime(to_date, '%Y-%m-%d').date()
                if parsed_to < today:
                    errors.append('To date cannot be in the past')
            except ValueError:
                errors.append('Invalid to date format')
        
        # Check date range validity
        if from_date and to_date and not errors:
            parsed_from = datetime.strptime(from_date, '%Y-%m-%d').date()
            parsed_to = datetime.strptime(to_date, '%Y-%m-%d').date()
            if parsed_to < parsed_from:
                errors.append('To date must be after or equal to From date')
            elif (parsed_to - parsed_from).days > 30:
                errors.append('Leave duration cannot exceed 30 days')
        
        if not leave_type:
            errors.append('Leave type is required')
        elif leave_type not in ['PLANNED', 'CASUAL', 'EMERGENCY', 'SICK']:
            errors.append('Invalid leave type')
        
        if errors:
            return JsonResponse({'success': False, 'errors': errors})
        
        ip_address = get_client_ip(request)
        user_agent = get_user_agent(request)
        
        # Create leave with date range
        leave_id, editable_until, total_days = models.create_leave(
            user['id'], from_date, to_date, leave_type, notes,
            ip_address=ip_address, user_agent=user_agent
        )
        
        # Get created leave for email
        leave_data = models.get_leave_by_id(leave_id)
        
        # Send email notification to admin
        try:
            email_success, email_msg = emails.send_new_leave_notification(leave_data)
            if email_success:
                models.mark_email_sent_admin(leave_id)
            else:
                logger.warning(f"New leave email failed: {email_msg}")
        except Exception as e:
            logger.error(f"Error sending new leave email: {e}")
        
        return JsonResponse({
            'success': True,
            'message': f'Leave request submitted successfully ({total_days} day{"s" if total_days > 1 else ""})',
            'id': leave_id,
            'total_days': total_days,
            'editable_until': models.format_ist_datetime(editable_until),
            'seconds_remaining': models.EDIT_WINDOW_MINUTES * 60
        })
        
    except Exception as e:
        logger.exception("Error creating leave")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ============================================
# USER EDIT LEAVE
# ============================================

@user_login_required
@require_POST
def leave_edit_user_v2(request, leave_id):
    """Edit leave request with date range within edit window (AJAX)"""
    user = request.current_user
    
    try:
        data = json.loads(request.body)
        from_date = data.get('from_date', '').strip()
        to_date = data.get('to_date', '').strip()
        leave_type = data.get('leave_type', '').strip().upper()
        notes = data.get('notes', '').strip()
        
        # Validation
        errors = []
        today = models.get_ist_now().date()
        
        if not from_date:
            errors.append('From date is required')
        else:
            try:
                parsed_from = datetime.strptime(from_date, '%Y-%m-%d').date()
                if parsed_from < today:
                    errors.append('From date cannot be in the past')
            except ValueError:
                errors.append('Invalid from date format')
        
        if not to_date:
            errors.append('To date is required')
        else:
            try:
                parsed_to = datetime.strptime(to_date, '%Y-%m-%d').date()
                if parsed_to < today:
                    errors.append('To date cannot be in the past')
            except ValueError:
                errors.append('Invalid to date format')
        
        # Check date range validity
        if from_date and to_date and not errors:
            parsed_from = datetime.strptime(from_date, '%Y-%m-%d').date()
            parsed_to = datetime.strptime(to_date, '%Y-%m-%d').date()
            if parsed_to < parsed_from:
                errors.append('To date must be after or equal to From date')
            elif (parsed_to - parsed_from).days > 30:
                errors.append('Leave duration cannot exceed 30 days')
        
        if not leave_type:
            errors.append('Leave type is required')
        elif leave_type not in ['PLANNED', 'CASUAL', 'EMERGENCY', 'SICK']:
            errors.append('Invalid leave type')
        
        if errors:
            return JsonResponse({'success': False, 'errors': errors})
        
        ip_address = get_client_ip(request)
        user_agent = get_user_agent(request)
        
        # Update leave with date range (will check edit window)
        success, message = models.update_leave_user(
            leave_id, user['id'], from_date, to_date, leave_type, notes,
            ip_address=ip_address, user_agent=user_agent
        )
        
        if not success:
            return JsonResponse({'success': False, 'error': message}, status=403)
        
        # Get updated leave for email
        leave_data = models.get_leave_by_id(leave_id)
        
        # Send edit notification to admin
        try:
            emails.send_leave_edited_notification(leave_data)
        except Exception as e:
            logger.error(f"Error sending edit notification: {e}")
        
        return JsonResponse({'success': True, 'message': message})
        
    except Exception as e:
        logger.exception(f"Error editing leave {leave_id}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ============================================
# USER CANCEL LEAVE
# ============================================

@user_login_required
@require_POST
def leave_cancel_user_v2(request, leave_id):
    """Cancel leave request (AJAX)"""
    user = request.current_user
    
    try:
        data = json.loads(request.body) if request.body else {}
        reason = data.get('reason', 'Cancelled by user')
        
        ip_address = get_client_ip(request)
        user_agent = get_user_agent(request)
        
        success, message = models.cancel_leave_user(
            leave_id, user['id'], reason,
            ip_address=ip_address, user_agent=user_agent
        )
        
        if not success:
            return JsonResponse({'success': False, 'error': message}, status=403)
        
        return JsonResponse({'success': True, 'message': message})
        
    except Exception as e:
        logger.exception(f"Error cancelling leave {leave_id}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ============================================
# USER CHECK EDIT WINDOW
# ============================================

@user_login_required
def leave_check_edit_window(request, leave_id):
    """Check if leave is still editable (AJAX)"""
    user = request.current_user
    
    is_editable, message, seconds_remaining = models.check_edit_window(leave_id, user['id'])
    
    return JsonResponse({
        'success': True,
        'is_editable': is_editable,
        'message': message,
        'seconds_remaining': seconds_remaining
    })
