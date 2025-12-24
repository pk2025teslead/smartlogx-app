from django.urls import path
from . import views
from . import attendance_views
from . import leave_views

app_name = 'userpanel'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Log Management
    path('logs/', views.log_manage_view, name='log_manage'),
    path('logs/<int:log_id>/', views.get_log_detail, name='log_detail'),
    path('logs/save/', views.save_log, name='save_log'),
    
    # Time Window & Approval
    path('logs/check-time/', views.check_time_window, name='check_time'),
    path('logs/request-approval/', views.request_approval_code, name='request_approval'),
    path('logs/verify-code/', views.verify_approval_code, name='verify_code'),
    
    # Attendance Dashboard
    path('attendance/', attendance_views.attendance_dashboard, name='attendance'),
    
    # ============================================
    # LEAVE MANAGEMENT - Enhanced with Edit Window & Audit
    # ============================================
    path('attendance/leave/', leave_views.leave_list_user_v2, name='leave_list'),
    path('attendance/leave/<int:leave_id>/', leave_views.leave_detail_user_v2, name='leave_detail'),
    path('attendance/leave/create/', leave_views.leave_create_user_v2, name='leave_create'),
    path('attendance/leave/<int:leave_id>/edit/', leave_views.leave_edit_user_v2, name='leave_edit'),
    path('attendance/leave/<int:leave_id>/cancel/', leave_views.leave_cancel_user_v2, name='leave_cancel'),
    path('attendance/leave/<int:leave_id>/check-edit/', leave_views.leave_check_edit_window, name='leave_check_edit'),
    
    # Comp-Off Management
    path('attendance/compoff/', attendance_views.compoff_list, name='compoff_list'),
    path('attendance/compoff/<int:compoff_id>/', attendance_views.get_compoff_detail, name='compoff_detail'),
    path('attendance/compoff/save/', attendance_views.save_compoff, name='save_compoff'),
    path('attendance/compoff/<int:compoff_id>/delete/', attendance_views.delete_compoff, name='delete_compoff'),
    
    # WFH Management
    path('attendance/wfh/', attendance_views.wfh_list, name='wfh_list'),
    path('attendance/wfh/<int:wfh_id>/', attendance_views.get_wfh_detail, name='wfh_detail'),
    path('attendance/wfh/save/', attendance_views.save_wfh, name='save_wfh'),
    path('attendance/wfh/<int:wfh_id>/delete/', attendance_views.delete_wfh, name='delete_wfh'),
    
    # Column Order Save
    path('save-column-order/', attendance_views.save_column_order, name='save_column_order'),
]
