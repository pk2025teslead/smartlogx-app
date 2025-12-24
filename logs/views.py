from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Log
import json
from datetime import datetime

@login_required
def dashboard_view(request):
    """User dashboard with logs display"""
    # Fetch user logs using raw SQL
    logs = Log.get_user_logs_raw(request.user.id)
    
    # Get monthly statistics
    monthly_stats = Log.get_monthly_stats_raw(request.user.id)
    
    # Get priority statistics
    priority_stats = Log.get_priority_stats_raw(request.user.id)
    
    # Convert to format suitable for Chart.js
    months = [stat['month'] for stat in monthly_stats]
    counts = [stat['count'] for stat in monthly_stats]
    
    priority_data = {
        'Low': 0,
        'Medium': 0,
        'High': 0
    }
    for stat in priority_stats:
        priority_data[stat['priority']] = stat['count']
    
    context = {
        'logs': logs,
        'total_logs': len(logs),
        'monthly_stats': json.dumps({'months': months, 'counts': counts}),
        'priority_stats': json.dumps(priority_data),
        'user': request.user
    }
    
    return render(request, 'logs/dashboard.html', context)

@login_required
def add_log_view(request):
    """Add new log"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        priority = request.POST.get('priority', 'Low')
        log_date = request.POST.get('log_date')

        # Validation
        if not title or not log_date:
            messages.error(request, 'Title and log date are required.')
            return redirect('/logs/dashboard/')

        # Insert log using raw SQL
        try:
            Log.create_log_raw(
                user_id=request.user.id,
                title=title,
                description=description,
                priority=priority,
                log_date=log_date
            )
            messages.success(request, 'Log added successfully!')
        except Exception as e:
            messages.error(request, f'Error adding log: {str(e)}')

        return redirect('/logs/dashboard/')

    return redirect('/logs/dashboard/')

@login_required
def edit_log_view(request, log_id):
    """Edit existing log"""
    # Fetch log using raw SQL
    log = Log.get_log_by_id_raw(log_id, request.user.id)
    
    if not log:
        messages.error(request, 'Log not found or you do not have permission to edit it.')
        return redirect('/logs/dashboard/')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        priority = request.POST.get('priority', 'Low')
        log_date = request.POST.get('log_date')

        # Validation
        if not title or not log_date:
            messages.error(request, 'Title and log date are required.')
            return render(request, 'logs/edit_log.html', {'log': log})

        # Update log using raw SQL
        try:
            success = Log.update_log_raw(
                log_id=log_id,
                user_id=request.user.id,
                title=title,
                description=description,
                priority=priority,
                log_date=log_date
            )
            if success:
                messages.success(request, 'Log updated successfully!')
                return redirect('/logs/dashboard/')
            else:
                messages.error(request, 'Failed to update log.')
        except Exception as e:
            messages.error(request, f'Error updating log: {str(e)}')

    return render(request, 'logs/edit_log.html', {'log': log})

@login_required
def delete_log_view(request, log_id):
    """Delete log"""
    if request.method == 'POST':
        try:
            success = Log.delete_log_raw(log_id, request.user.id)
            if success:
                messages.success(request, 'Log deleted successfully!')
            else:
                messages.error(request, 'Log not found or you do not have permission to delete it.')
        except Exception as e:
            messages.error(request, f'Error deleting log: {str(e)}')

    return redirect('/logs/dashboard/')

@login_required
def get_log_api(request, log_id):
    """API endpoint to get log details (for AJAX)"""
    log = Log.get_log_by_id_raw(log_id, request.user.id)
    
    if log:
        # Convert datetime objects to strings
        log['log_date'] = log['log_date'].strftime('%Y-%m-%d') if log['log_date'] else ''
        log['created_at'] = log['created_at'].strftime('%Y-%m-%d %H:%M:%S') if log['created_at'] else ''
        log['updated_at'] = log['updated_at'].strftime('%Y-%m-%d %H:%M:%S') if log['updated_at'] else ''
        return JsonResponse({'success': True, 'log': log})
    
    return JsonResponse({'success': False, 'message': 'Log not found'})

@login_required
def timeline_view(request):
    """Timeline view of logs"""
    logs = Log.get_user_logs_raw(request.user.id)
    
    context = {
        'logs': logs,
        'user': request.user
    }
    
    return render(request, 'logs/timeline.html', context)
