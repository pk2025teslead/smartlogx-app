"""
URL configuration for smartlogx project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
from django.contrib.auth.models import User
from decouple import config

@csrf_exempt
def setup_database_view(request):
    """Setup database after deployment"""
    try:
        from logs.models import Log
        
        # Run migrations
        print("Running migrations...")
        call_command('migrate', verbosity=2)
        
        # Create superuser if doesn't exist
        if not User.objects.filter(is_superuser=True).exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email=config('ADMIN_EMAIL', default='admin@smartlogx.com'),
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            admin_created = True
        else:
            admin_user = User.objects.filter(is_superuser=True).first()
            admin_created = False
        
        # Create sample users
        sample_users_created = 0
        sample_users = [
            {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
        ]
        
        for user_data in sample_users:
            if not User.objects.filter(username=user_data['username']).exists():
                User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password='password123',
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name']
                )
                sample_users_created += 1
        
        # Create sample logs
        sample_logs_created = 0
        if User.objects.exists():
            users = User.objects.all()[:2]  # Get first 2 users
            for user in users:
                if not Log.objects.filter(user=user).exists():
                    Log.objects.create(
                        user=user,
                        title='Welcome to SmartLogX',
                        description='This is your first log entry. You can edit or delete this.',
                        priority='Medium',
                        log_date='2024-12-24'
                    )
                    sample_logs_created += 1
        
        return JsonResponse({
            'status': 'success',
            'message': 'Database setup completed successfully!',
            'details': {
                'admin_created': admin_created,
                'sample_users_created': sample_users_created,
                'sample_logs_created': sample_logs_created,
                'total_users': User.objects.count(),
                'total_logs': Log.objects.count(),
                'login_info': {
                    'admin': 'admin / admin123',
                    'users': 'john_doe, jane_smith / password123'
                }
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error', 
            'message': f'Setup failed: {str(e)}',
            'error_type': type(e).__name__
        })

def debug_database_view(request):
    """Debug database status"""
    try:
        from logs.models import Log
        
        users_count = User.objects.count()
        logs_count = Log.objects.count()
        admin_count = User.objects.filter(is_superuser=True).count()
        
        # Get admin user details
        admin_exists = False
        admin_details = {}
        try:
            admin = User.objects.get(username='admin')
            admin_exists = True
            admin_details = {
                'username': admin.username,
                'email': admin.email,
                'is_active': admin.is_active,
                'is_superuser': admin.is_superuser,
                'is_staff': admin.is_staff
            }
        except User.DoesNotExist:
            pass
        
        return JsonResponse({
            'status': 'success',
            'database_status': {
                'total_users': users_count,
                'total_logs': logs_count,
                'admin_users': admin_count,
                'admin_exists': admin_exists,
                'admin_details': admin_details
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include('accounts.urls')),
    path("logs/", include('logs.urls')),
    path("adminpanel/", include('adminpanel.urls')),
    path("user/", include('userpanel.urls')),
    path("setup-db/", setup_database_view, name='setup_database'),
    path("debug-db/", debug_database_view, name='debug_database'),
    # Landing page commented - direct to login
    # path("", include('public.urls')),
    path("", lambda request: redirect('/accounts/login/')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

