from django.urls import path
from . import views

app_name = 'logs'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add/', views.add_log_view, name='add_log'),
    path('edit/<int:log_id>/', views.edit_log_view, name='edit_log'),
    path('delete/<int:log_id>/', views.delete_log_view, name='delete_log'),
    path('api/get/<int:log_id>/', views.get_log_api, name='get_log_api'),
    path('timeline/', views.timeline_view, name='timeline'),
]
