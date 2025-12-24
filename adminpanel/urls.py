from django.urls import path
from . import views
from . import attendance_views
from . import leave_views

app_name = 'adminpanel'

urlpatterns = [
    # Main Dashboard
    path('dashboard/', attendance_views.admin_dashboard, name='dashboard'),
    
    # User Management (existing)
    path('users/', views.user_list_view, name='user_list'),
    path('users/add/', views.add_user_view, name='add_user'),
    path('users/<int:user_id>/edit/', views.edit_user_view, name='edit_user'),
    path('users/<int:user_id>/delete/', views.delete_user_view, name='delete_user'),
    path('users/<int:user_id>/reset-password/', views.reset_password_view, name='reset_password'),
    
    # First Login Password Change
    path('change-password/', views.change_password_view, name='change_password'),
    
    # ============================================
    # LEAVE MANAGEMENT - Enhanced with Edit Window & Audit
    # ============================================
    path('attendance/leave/', leave_views.leave_list_admin_v2, name='leave_list'),
    path('attendance/leave/list/', leave_views.leave_list_json_v2, name='leave_list_json'),
    path('attendance/leave/<int:leave_id>/', leave_views.leave_detail_admin_v2, name='leave_detail'),
    path('attendance/leave/<int:leave_id>/update/', leave_views.leave_update_admin_v2, name='leave_update'),
    path('attendance/leave/<int:leave_id>/delete/', leave_views.leave_delete_admin_v2, name='leave_delete'),
    path('attendance/leave/<int:leave_id>/approve/', leave_views.leave_approve_admin_v2, name='leave_approve'),
    path('attendance/leave/<int:leave_id>/reject/', leave_views.leave_reject_admin_v2, name='leave_reject'),
    path('attendance/leave/<int:leave_id>/audit/', leave_views.leave_audit_admin, name='leave_audit'),
    
    # ============================================
    # ATTENDANCE MANAGEMENT - Comp-Off
    # ============================================
    path('attendance/compoff/', attendance_views.compoff_list_admin, name='compoff_list'),
    path('attendance/compoff/<int:compoff_id>/', attendance_views.compoff_detail_admin, name='compoff_detail'),
    path('attendance/compoff/<int:compoff_id>/update/', attendance_views.compoff_update_admin, name='compoff_update'),
    path('attendance/compoff/<int:compoff_id>/delete/', attendance_views.compoff_delete_admin, name='compoff_delete'),
    path('attendance/compoff/<int:compoff_id>/approve/', attendance_views.compoff_approve_admin, name='compoff_approve'),
    
    # ============================================
    # ATTENDANCE MANAGEMENT - WFH
    # ============================================
    path('attendance/wfh/', attendance_views.wfh_list_admin, name='wfh_list'),
    path('attendance/wfh/<int:wfh_id>/', attendance_views.wfh_detail_admin, name='wfh_detail'),
    path('attendance/wfh/<int:wfh_id>/update/', attendance_views.wfh_update_admin, name='wfh_update'),
    path('attendance/wfh/<int:wfh_id>/delete/', attendance_views.wfh_delete_admin, name='wfh_delete'),
    path('attendance/wfh/<int:wfh_id>/approve/', attendance_views.wfh_approve_admin, name='wfh_approve'),
    
    # ============================================
    # LOG MANAGEMENT
    # ============================================
    path('logs/', attendance_views.log_list_admin, name='log_list'),
    path('logs/<int:log_id>/', attendance_views.log_detail_admin, name='log_detail'),
    
    # Profile
    path('profile/update/', views.profile_update_view, name='profile_update'),
    
    # Legacy routes (existing)
    path('filter-logs/', views.filter_logs_view, name='filter_logs'),
    path('manage-users/', views.manage_users_view, name='manage_users'),
    path('toggle-user/<int:user_id>/', views.toggle_user_status, name='toggle_user'),
    path('export/csv/', views.export_logs_csv, name='export_csv'),
    path('export/excel/', views.export_logs_excel, name='export_excel'),
    path('analytics/', views.analytics_view, name='analytics'),
]
