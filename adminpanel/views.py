from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from logs.models import Log
from accounts.models import UserProfile
from .email_utils import generate_temp_password, send_welcome_email, send_password_reset_email
import json
import csv
from openpyxl import Workbook
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def is_admin(user):
    """Check if user is admin/staff"""
    return user.is_staff


# ============================================
# Raw SQL Helper Functions for users_master
# ============================================

def get_all_users():
    """Get all users from users_master table"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ID, EMP_ID, EMP_NAME, MOBILE_NUMBER, EMAIL, ROLE, ROLL, 
                   IS_FIRST_LOGIN, CREATED_AT, UPDATED_AT
            FROM users_master
            ORDER BY CREATED_AT DESC
        """)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_user_by_id(user_id):
    """Get single user by ID"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ID, EMP_ID, EMP_NAME, MOBILE_NUMBER, EMAIL, ROLE, ROLL, 
                   IS_FIRST_LOGIN, CREATED_AT, UPDATED_AT
            FROM users_master
            WHERE ID = %s
        """, [user_id])
        row = cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))
    return None


def get_user_by_emp_id(emp_id):
    """Get user by EMP_ID"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ID, EMP_ID, EMP_NAME, MOBILE_NUMBER, EMAIL, ROLE, ROLL, 
                   PASSWORD, IS_FIRST_LOGIN, CREATED_AT, UPDATED_AT
            FROM users_master
            WHERE EMP_ID = %s
        """, [emp_id])
        row = cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))
    return None


def get_user_by_email(email):
    """Get user by email"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ID, EMP_ID, EMP_NAME, MOBILE_NUMBER, EMAIL, ROLE, ROLL, 
                   PASSWORD, IS_FIRST_LOGIN, CREATED_AT, UPDATED_AT
            FROM users_master
            WHERE EMAIL = %s
        """, [email])
        row = cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))
    return None


def create_user(emp_id, emp_name, mobile_number, email, role, roll, password):
    """Create new user in users_master"""
    hashed_password = make_password(password)
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO users_master 
            (EMP_ID, EMP_NAME, MOBILE_NUMBER, EMAIL, ROLE, ROLL, PASSWORD, IS_FIRST_LOGIN, CREATED_AT, UPDATED_AT)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 1, NOW(), NOW())
        """, [emp_id, emp_name, mobile_number, email, role, roll, hashed_password])
        return cursor.lastrowid


def update_user(user_id, emp_id, emp_name, mobile_number, email, role, roll):
    """Update user details (without password)"""
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE users_master
            SET EMP_ID = %s, EMP_NAME = %s, MOBILE_NUMBER = %s, EMAIL = %s, 
                ROLE = %s, ROLL = %s, UPDATED_AT = NOW()
            WHERE ID = %s
        """, [emp_id, emp_name, mobile_number, email, role, roll, user_id])
        return cursor.rowcount


def delete_user(user_id):
    """Delete user from users_master"""
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM users_master WHERE ID = %s", [user_id])
        return cursor.rowcount


def reset_user_password(user_id, new_password='Temp@123'):
    """Reset user password and set IS_FIRST_LOGIN to True"""
    hashed_password = make_password(new_password)
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE users_master
            SET PASSWORD = %s, IS_FIRST_LOGIN = 1, UPDATED_AT = NOW()
            WHERE ID = %s
        """, [hashed_password, user_id])
        return cursor.rowcount


def update_user_password(user_id, new_password):
    """Update user password and set IS_FIRST_LOGIN to False"""
    hashed_password = make_password(new_password)
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE users_master
            SET PASSWORD = %s, IS_FIRST_LOGIN = 0, UPDATED_AT = NOW()
            WHERE ID = %s
        """, [hashed_password, user_id])
        return cursor.rowcount


def get_users_count_by_role():
    """Get user count grouped by role"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ROLE, COUNT(*) as count
            FROM users_master
            GROUP BY ROLE
        """)
        return {row[0]: row[1] for row in cursor.fetchall()}


# ============================================
# Admin Panel Views
# ============================================

@login_required
@user_passes_test(is_admin)
def dashboard_view(request):
    """Admin dashboard with all logs and analytics"""
    logs = Log.get_all_logs_raw()
    users = UserProfile.get_all_users_raw()
    priority_stats = Log.get_priority_stats_raw()
    
    priority_data = {'Low': 0, 'Medium': 0, 'High': 0}
    for stat in priority_stats:
        priority_data[stat['priority']] = stat['count']
    
    context = {
        'logs': logs,
        'users': users,
        'total_logs': len(logs),
        'total_users': len(users),
        'priority_stats': json.dumps(priority_data),
    }
    
    return render(request, 'adminpanel/dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def user_list_view(request):
    """User list page with Zoho-style table"""
    users = get_all_users()
    role_counts = get_users_count_by_role()
    
    roles = [
        'SOFTWARE DEVELOPER',
        'SOFTWARE TESTER',
        'UI UX DESIGNER',
        'IT COORDINATOR'
    ]
    
    context = {
        'users': users,
        'total_users': len(users),
        'role_counts': role_counts,
        'roles': roles,
    }
    
    return render(request, 'adminpanel/user_list.html', context)


@login_required
@user_passes_test(is_admin)
def add_user_view(request):
    """Add new user page with auto-generated temp password and welcome email"""
    roles = [
        'SOFTWARE DEVELOPER',
        'SOFTWARE TESTER',
        'UI UX DESIGNER',
        'IT COORDINATOR'
    ]
    
    if request.method == 'POST':
        emp_id = request.POST.get('emp_id', '').strip()
        emp_name = request.POST.get('emp_name', '').strip()
        mobile_number = request.POST.get('mobile_number', '').strip()
        email = request.POST.get('email', '').strip()
        role = request.POST.get('role', '').strip()
        roll = request.POST.get('roll', '').strip()
        
        # Server-side validation
        errors = []
        
        if not emp_id:
            errors.append('Employee ID is required')
        elif get_user_by_emp_id(emp_id):
            errors.append('Employee ID already exists')
            
        if not emp_name:
            errors.append('Employee Name is required')
            
        if not email:
            errors.append('Email is required')
        elif get_user_by_email(email):
            errors.append('Email already exists')
            
        if not role:
            errors.append('Role is required')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'adminpanel/add_user.html', {
                'roles': roles,
                'form_data': request.POST
            })
        
        try:
            # Generate secure temporary password
            temp_password = generate_temp_password(10)
            
            # Create user with hashed password (raw SQL)
            create_user(emp_id, emp_name, mobile_number, email, role, roll, temp_password)
            
            # Send welcome email with credentials
            email_success, email_message = send_welcome_email(
                user_email=email,
                user_name=emp_name,
                username=emp_id,  # Using EMP_ID as username
                temp_password=temp_password
            )
            
            if email_success:
                messages.success(request, f'User {emp_name} created successfully! Welcome email sent to {email}.')
            else:
                # User created but email failed - still success but warn admin
                messages.warning(request, f'User {emp_name} created successfully, but email could not be sent: {email_message}')
                logger.error(f"Failed to send welcome email to {email}: {email_message}")
            
            return redirect('adminpanel:user_list')
            
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
            logger.exception(f"Error creating user {emp_name}")
    
    return render(request, 'adminpanel/add_user.html', {'roles': roles})


@login_required
@user_passes_test(is_admin)
def edit_user_view(request, user_id):
    """Edit user page"""
    user = get_user_by_id(user_id)
    
    if not user:
        messages.error(request, 'User not found')
        return redirect('adminpanel:user_list')
    
    roles = [
        'SOFTWARE DEVELOPER',
        'SOFTWARE TESTER',
        'UI UX DESIGNER',
        'IT COORDINATOR'
    ]
    
    if request.method == 'POST':
        emp_id = request.POST.get('emp_id', '').strip()
        emp_name = request.POST.get('emp_name', '').strip()
        mobile_number = request.POST.get('mobile_number', '').strip()
        email = request.POST.get('email', '').strip()
        role = request.POST.get('role', '').strip()
        roll = request.POST.get('roll', '').strip()
        
        # Server-side validation
        errors = []
        
        if not emp_id:
            errors.append('Employee ID is required')
        else:
            existing = get_user_by_emp_id(emp_id)
            if existing and existing['ID'] != user_id:
                errors.append('Employee ID already exists')
            
        if not emp_name:
            errors.append('Employee Name is required')
            
        if not email:
            errors.append('Email is required')
        else:
            existing = get_user_by_email(email)
            if existing and existing['ID'] != user_id:
                errors.append('Email already exists')
            
        if not role:
            errors.append('Role is required')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'adminpanel/edit_user.html', {
                'user': user,
                'roles': roles
            })
        
        try:
            update_user(user_id, emp_id, emp_name, mobile_number, email, role, roll)
            messages.success(request, f'User {emp_name} updated successfully!')
            return redirect('adminpanel:user_list')
        except Exception as e:
            messages.error(request, f'Error updating user: {str(e)}')
    
    return render(request, 'adminpanel/edit_user.html', {
        'user': user,
        'roles': roles
    })


@login_required
@user_passes_test(is_admin)
@require_POST
def delete_user_view(request, user_id):
    """Delete user"""
    user = get_user_by_id(user_id)
    
    if not user:
        messages.error(request, 'User not found')
        return redirect('adminpanel:user_list')
    
    try:
        delete_user(user_id)
        messages.success(request, f'User {user["EMP_NAME"]} deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting user: {str(e)}')
    
    return redirect('adminpanel:user_list')


@login_required
@user_passes_test(is_admin)
@require_POST
def reset_password_view(request, user_id):
    """Reset user password with auto-generated temp password and email notification"""
    user = get_user_by_id(user_id)
    
    if not user:
        messages.error(request, 'User not found')
        return redirect('adminpanel:user_list')
    
    try:
        # Generate new temporary password
        temp_password = generate_temp_password(10)
        
        # Reset password in database
        reset_user_password(user_id, temp_password)
        
        # Send password reset email notification
        if user.get('EMAIL'):
            email_success, email_message = send_password_reset_email(
                user_email=user['EMAIL'],
                user_name=user['EMP_NAME'],
                username=user['EMP_ID'],
                temp_password=temp_password
            )
            
            if email_success:
                messages.success(request, f'Password for {user["EMP_NAME"]} reset successfully! Email notification sent.')
            else:
                messages.warning(request, f'Password reset for {user["EMP_NAME"]}, but email could not be sent: {email_message}')
                logger.error(f"Failed to send password reset email to {user['EMAIL']}: {email_message}")
        else:
            messages.success(request, f'Password for {user["EMP_NAME"]} reset successfully! (No email on file)')
            
    except Exception as e:
        messages.error(request, f'Error resetting password: {str(e)}')
        logger.exception(f"Error resetting password for user {user_id}")
    
    return redirect('adminpanel:user_list')


# ============================================
# First Login Password Change (User Side)
# ============================================

def change_password_view(request):
    """First login password change page"""
    # Get user from session (set during login)
    user_id = request.session.get('first_login_user_id')
    
    if not user_id:
        messages.error(request, 'Invalid session. Please login again.')
        return redirect('accounts:login')
    
    user = get_user_by_id(user_id)
    
    if not user:
        messages.error(request, 'User not found')
        return redirect('accounts:login')
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        
        errors = []
        
        if not new_password:
            errors.append('New password is required')
        elif len(new_password) < 6:
            errors.append('Password must be at least 6 characters')
            
        if new_password != confirm_password:
            errors.append('Passwords do not match')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'adminpanel/change_password.html', {'user': user})
        
        try:
            update_user_password(user_id, new_password)
            # Clear the session flag
            del request.session['first_login_user_id']
            messages.success(request, 'Password changed successfully! Please login with your new password.')
            return redirect('accounts:login')
        except Exception as e:
            messages.error(request, f'Error changing password: {str(e)}')
    
    return render(request, 'adminpanel/change_password.html', {'user': user})


# ============================================
# Existing Views (Updated)
# ============================================

@login_required
@user_passes_test(is_admin)
def filter_logs_view(request):
    """Filter logs by user, date, priority"""
    user_id = request.GET.get('user_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    priority = request.GET.get('priority')
    
    logs = Log.get_logs_by_filter_raw(
        user_id=user_id if user_id else None,
        start_date=start_date if start_date else None,
        end_date=end_date if end_date else None,
        priority=priority if priority else None
    )
    
    users = UserProfile.get_all_users_raw()
    
    context = {
        'logs': logs,
        'users': users,
        'filters': {
            'user_id': user_id,
            'start_date': start_date,
            'end_date': end_date,
            'priority': priority
        }
    }
    
    return render(request, 'adminpanel/filter_logs.html', context)


@login_required
@user_passes_test(is_admin)
def manage_users_view(request):
    """Manage users - activate/deactivate"""
    users = UserProfile.get_all_users_raw()
    return render(request, 'adminpanel/manage_users.html', {'users': users})


@login_required
@user_passes_test(is_admin)
def toggle_user_status(request, user_id):
    """Toggle user active status"""
    if request.method == 'POST':
        status = request.POST.get('status') == 'true'
        try:
            UserProfile.toggle_user_status_raw(user_id, status)
            messages.success(request, 'User status updated successfully.')
        except Exception as e:
            messages.error(request, f'Error updating user status: {str(e)}')
    return redirect('/adminpanel/manage-users/')


@login_required
@user_passes_test(is_admin)
def export_logs_csv(request):
    """Export logs to CSV"""
    user_id = request.GET.get('user_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    priority = request.GET.get('priority')
    
    logs = Log.get_logs_by_filter_raw(
        user_id=user_id if user_id else None,
        start_date=start_date if start_date else None,
        end_date=end_date if end_date else None,
        priority=priority if priority else None
    )
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="logs_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'User', 'Email', 'Title', 'Description', 'Priority', 'Log Date', 'Created At'])
    
    for log in logs:
        writer.writerow([
            log['id'],
            log['username'],
            log['email'],
            log['title'],
            log['description'],
            log['priority'],
            log['log_date'].strftime('%Y-%m-%d') if log['log_date'] else '',
            log['created_at'].strftime('%Y-%m-%d %H:%M:%S') if log['created_at'] else ''
        ])
    
    return response


@login_required
@user_passes_test(is_admin)
def export_logs_excel(request):
    """Export logs to Excel"""
    user_id = request.GET.get('user_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    priority = request.GET.get('priority')
    
    logs = Log.get_logs_by_filter_raw(
        user_id=user_id if user_id else None,
        start_date=start_date if start_date else None,
        end_date=end_date if end_date else None,
        priority=priority if priority else None
    )
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Logs Export"
    
    headers = ['ID', 'User', 'Email', 'Title', 'Description', 'Priority', 'Log Date', 'Created At']
    ws.append(headers)
    
    for log in logs:
        ws.append([
            log['id'],
            log['username'],
            log['email'],
            log['title'],
            log['description'],
            log['priority'],
            log['log_date'].strftime('%Y-%m-%d') if log['log_date'] else '',
            log['created_at'].strftime('%Y-%m-%d %H:%M:%S') if log['created_at'] else ''
        ])
    
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="logs_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
    
    wb.save(response)
    return response


@login_required
@user_passes_test(is_admin)
def analytics_view(request):
    """Admin analytics page"""
    all_logs = Log.get_all_logs_raw()
    priority_stats = Log.get_priority_stats_raw()
    
    priority_data = {'Low': 0, 'Medium': 0, 'High': 0}
    for stat in priority_stats:
        priority_data[stat['priority']] = stat['count']
    
    context = {
        'total_logs': len(all_logs),
        'priority_stats': json.dumps(priority_data),
    }
    
    return render(request, 'adminpanel/analytics.html', context)


# ============================================
# Profile Update View
# ============================================

@login_required
@user_passes_test(is_admin)
@require_POST
def profile_update_view(request):
    """Update admin profile"""
    try:
        user = request.user
        
        # Get form data
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        current_password = request.POST.get('current_password', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        
        # Update basic info
        if email:
            user.email = email
        user.first_name = first_name
        user.last_name = last_name
        
        # Handle password change
        if new_password:
            if not current_password:
                return JsonResponse({'success': False, 'error': 'Current password is required'})
            
            if not user.check_password(current_password):
                return JsonResponse({'success': False, 'error': 'Current password is incorrect'})
            
            if new_password != confirm_password:
                return JsonResponse({'success': False, 'error': 'New passwords do not match'})
            
            if len(new_password) < 6:
                return JsonResponse({'success': False, 'error': 'Password must be at least 6 characters'})
            
            user.set_password(new_password)
        
        # Handle profile photo
        if 'profile_photo' in request.FILES:
            photo = request.FILES['profile_photo']
            # Save photo to media folder
            import os
            from django.conf import settings
            
            # Create profile_photos directory if not exists
            photo_dir = os.path.join(settings.MEDIA_ROOT, 'profile_photos')
            os.makedirs(photo_dir, exist_ok=True)
            
            # Save file
            filename = f"admin_{user.id}_{photo.name}"
            filepath = os.path.join(photo_dir, filename)
            
            with open(filepath, 'wb+') as destination:
                for chunk in photo.chunks():
                    destination.write(chunk)
            
            # Store photo path in session (or you can add a field to user model)
            request.session['profile_photo'] = f'/media/profile_photos/{filename}'
        
        user.save()
        
        return JsonResponse({
            'success': True, 
            'message': 'Profile updated successfully',
            'reload': bool(new_password)  # Reload if password changed
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
