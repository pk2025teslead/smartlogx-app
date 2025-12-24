"""
SmartLogX User Panel Views
Zoho Projects-style User Dashboard with Log Management
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages
from django.db import connection
from django.contrib.auth.hashers import check_password
from datetime import datetime, date, time
import pytz
import json
import random
import string

from . import models
from .notification_emails import send_log_submission_notification


# ============================================
# Timezone and Time Window Configuration
# ============================================

IST = pytz.timezone('Asia/Kolkata')

# Time windows for log submission (24-hour format)
FIRST_HALF_START = time(13, 0)   # 1:00 PM
FIRST_HALF_END = time(14, 30)    # 2:30 PM
SECOND_HALF_START = time(18, 0)  # 6:00 PM
SECOND_HALF_END = time(19, 30)   # 7:30 PM


def get_current_ist_time():
    """Get current time in IST"""
    return datetime.now(IST)


def is_within_time_window(session_type):
    """Check if current time is within allowed window for session type"""
    current_time = get_current_ist_time().time()
    
    if session_type == 'First Half':
        return FIRST_HALF_START <= current_time <= FIRST_HALF_END
    elif session_type == 'Second Half':
        return SECOND_HALF_START <= current_time <= SECOND_HALF_END
    return False


def get_time_window_info(session_type):
    """Get time window information for display"""
    if session_type == 'First Half':
        return {
            'start': '1:00 PM',
            'end': '2:30 PM',
            'start_24': '13:00',
            'end_24': '14:30'
        }
    elif session_type == 'Second Half':
        return {
            'start': '6:00 PM',
            'end': '7:30 PM',
            'start_24': '18:00',
            'end_24': '19:30'
        }
    return None


# ============================================
# User Authentication Helper
# ============================================

def get_current_user(request):
    """Get current user from session (users_master)"""
    user_id = request.session.get('user_master_id')
    if user_id:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT ID, EMP_ID, EMP_NAME, EMAIL, ROLE, ROLL
                FROM users_master WHERE ID = %s
            """, [user_id])
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'emp_id': row[1],
                    'emp_name': row[2],
                    'email': row[3],
                    'role': row[4],
                    'roll': row[5]
                }
    return None


def user_login_required(view_func):
    """Decorator to require user login from users_master"""
    def wrapper(request, *args, **kwargs):
        user = get_current_user(request)
        if not user:
            messages.error(request, 'Please login to continue.')
            return redirect('accounts:login')
        request.current_user = user
        return view_func(request, *args, **kwargs)
    return wrapper


# ============================================
# Dashboard View
# ============================================

@user_login_required
def dashboard_view(request):
    """Main user dashboard with modules"""
    user = request.current_user
    current_date = get_current_ist_time()
    
    # Get current month stats
    stats = models.get_user_log_stats(user['id'], current_date.year, current_date.month)
    
    context = {
        'user': user,
        'current_date': current_date,
        'stats': stats,
        'modules': [
            {
                'name': 'Log Manage',
                'icon': 'bi-journal-text',
                'url': 'userpanel:log_manage',
                'description': 'Manage your daily work logs',
                'active': True
            },
            {
                'name': 'Attendance',
                'icon': 'bi-calendar-check',
                'url': 'userpanel:attendance',
                'description': 'Leave, Comp-Off & WFH management',
                'active': True
            }
        ]
    }
    
    return render(request, 'userpanel/dashboard.html', context)


# ============================================
# Log Management Views
# ============================================

@user_login_required
def log_manage_view(request):
    """Log management page with month-wise logs"""
    user = request.current_user
    current_date = get_current_ist_time()
    
    # Get year and month from query params or use current
    year = int(request.GET.get('year', current_date.year))
    month = int(request.GET.get('month', current_date.month))
    
    # Get logs for the month
    logs = models.get_user_logs_by_month(user['id'], year, month)
    
    # Get stats
    stats = models.get_user_log_stats(user['id'], year, month)
    
    # Get user's previous projects for autocomplete
    user_projects = models.get_user_projects(user['id'])
    
    # Check current time window
    current_time = current_date.time()
    time_info = {
        'current_time': current_date.strftime('%H:%M'),
        'current_time_display': current_date.strftime('%I:%M %p'),
        'first_half_allowed': FIRST_HALF_START <= current_time <= FIRST_HALF_END,
        'second_half_allowed': SECOND_HALF_START <= current_time <= SECOND_HALF_END,
    }
    
    context = {
        'user': user,
        'logs': logs,
        'stats': stats,
        'year': year,
        'month': month,
        'month_name': date(year, month, 1).strftime('%B'),
        'current_date': current_date.strftime('%Y-%m-%d'),
        'current_date_display': current_date.strftime('%d %B %Y'),
        'user_projects': user_projects,
        'time_info': time_info,
        'is_current_month': year == current_date.year and month == current_date.month,
    }
    
    return render(request, 'userpanel/log_manage.html', context)


@user_login_required
def get_log_detail(request, log_id):
    """Get log details for view modal (AJAX)"""
    user = request.current_user
    log = models.get_log_by_id(log_id, user['id'])
    
    if not log:
        return JsonResponse({'success': False, 'error': 'Log not found'}, status=404)
    
    # Format dates for display
    log_data = {
        'id': log['ID'],
        'project_title': log['PROJECT_TITLE'],
        'log_heading': log['LOG_HEADING'],
        'log_details': log['LOG_DETAILS'],
        'log_date': log['LOG_DATE'].strftime('%d %B %Y') if log['LOG_DATE'] else '',
        'session_type': log['SESSION_TYPE'],
        'approval_required': log['APPROVAL_REQUIRED'],
        'created_at': log['CREATED_AT'].strftime('%d %B %Y, %I:%M %p') if log['CREATED_AT'] else ''
    }
    
    return JsonResponse({'success': True, 'log': log_data})


@user_login_required
@require_POST
def check_time_window(request):
    """Check if current time is within allowed window (AJAX)"""
    try:
        data = json.loads(request.body)
        session_type = data.get('session_type')
        
        if not session_type:
            return JsonResponse({'success': False, 'error': 'Session type required'})
        
        is_allowed = is_within_time_window(session_type)
        window_info = get_time_window_info(session_type)
        current_time = get_current_ist_time()
        
        return JsonResponse({
            'success': True,
            'is_allowed': is_allowed,
            'current_time': current_time.strftime('%I:%M %p'),
            'window_start': window_info['start'],
            'window_end': window_info['end'],
            'requires_approval': not is_allowed
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@user_login_required
@require_POST
def request_approval_code(request):
    """Generate and send approval code to admin (AJAX)"""
    user = request.current_user
    
    try:
        data = json.loads(request.body)
        session_type = data.get('session_type')
        
        if not session_type:
            return JsonResponse({'success': False, 'error': 'Session type required'})
        
        # Generate 6-digit code
        code = models.generate_approval_code()
        
        # Store code in database
        models.store_approval_code(user['id'], code, session_type)
        
        # Get admin email
        admin_email = models.get_admin_email()
        
        # ============================================
        # EMAIL SENDING CODE - UNCOMMENT IN PRODUCTION
        # ============================================
        # from django.core.mail import send_mail
        # from django.conf import settings
        #
        # subject = f'SmartLogX - Log Approval Code for {user["emp_name"]}'
        # message = f'''
        # Hello Admin,
        #
        # {user["emp_name"]} ({user["emp_id"]}) is requesting approval to submit a log outside the allowed time window.
        #
        # Session: {session_type}
        # Approval Code: {code}
        #
        # This code will expire in 15 minutes.
        #
        # - SmartLogX System
        # '''
        #
        # try:
        #     send_mail(
        #         subject,
        #         message,
        #         settings.DEFAULT_FROM_EMAIL,
        #         [admin_email],
        #         fail_silently=False,
        #     )
        # except Exception as e:
        #     return JsonResponse({'success': False, 'error': f'Failed to send email: {str(e)}'})
        # ============================================
        
        # For development/testing - log the code
        print(f"[DEV] Approval code for {user['emp_name']}: {code}")
        
        return JsonResponse({
            'success': True,
            'message': 'Approval code sent to admin. Please enter the code to proceed.',
            # Remove this in production - only for testing
            'dev_code': code
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@user_login_required
@require_POST
def verify_approval_code(request):
    """Verify the approval code entered by user (AJAX)"""
    user = request.current_user
    
    try:
        data = json.loads(request.body)
        code = data.get('code', '').strip()
        
        if not code or len(code) != 6:
            return JsonResponse({'success': False, 'error': 'Invalid code format'})
        
        result = models.verify_approval_code(user['id'], code)
        
        if result['valid']:
            return JsonResponse({
                'success': True,
                'message': 'Code verified successfully',
                'session_type': result['session_type']
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Invalid or expired code'
            })
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@user_login_required
@require_POST
def save_log(request):
    """Save a new log entry (AJAX)"""
    user = request.current_user
    
    try:
        data = json.loads(request.body)
        
        # Extract fields
        project_title = data.get('project_title', '').strip()
        log_heading = data.get('log_heading', '').strip()
        log_details = data.get('log_details', '').strip()
        session_type = data.get('session_type', '').strip()
        approval_used = data.get('approval_used', False)
        approval_code = data.get('approval_code', '').strip() if approval_used else None
        
        # Server-side validation
        errors = []
        
        if not project_title:
            errors.append('Project title is required')
        if not log_heading:
            errors.append('Log heading is required')
        if not log_details:
            errors.append('Log details are required')
        if session_type not in ['First Half', 'Second Half']:
            errors.append('Invalid session type')
        
        if errors:
            return JsonResponse({'success': False, 'errors': errors})
        
        # Verify time window (server-side)
        current_time = get_current_ist_time()
        is_allowed = is_within_time_window(session_type)
        
        if not is_allowed and not approval_used:
            return JsonResponse({
                'success': False,
                'error': 'Submission not allowed outside time window. Request approval first.'
            })
        
        # If approval was used, verify it was valid (code already consumed during verification)
        # The approval_used flag indicates the user went through the approval flow
        
        # Create the log
        log_date = current_time.date()
        log_id = models.create_user_log(
            user_id=user['id'],
            project_title=project_title,
            log_heading=log_heading,
            log_details=log_details,
            log_date=log_date,
            session_type=session_type,
            approval_required=approval_used,
            approval_code=approval_code
        )
        
        # Send email notification to admin
        try:
            formatted_date = log_date.strftime('%d %B %Y')
            
            email_success, email_msg = send_log_submission_notification(
                user_name=user['emp_name'],
                emp_id=user['emp_id'],
                log_date=formatted_date,
                project_title=project_title,
                log_heading=log_heading,
                session=session_type,
                description=log_details
            )
            
            if not email_success:
                print(f"[WARNING] Log notification email failed: {email_msg}")
        except Exception as email_error:
            print(f"[ERROR] Error sending log notification: {str(email_error)}")
        
        return JsonResponse({
            'success': True,
            'message': 'Log saved successfully!',
            'log_id': log_id
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ============================================
# Attendance Module (Placeholder)
# ============================================

@user_login_required
def attendance_view(request):
    """Attendance management - Coming Soon"""
    user = request.current_user
    
    context = {
        'user': user,
        'coming_soon': True
    }
    
    return render(request, 'userpanel/attendance.html', context)
