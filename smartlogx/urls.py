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
    """Setup database after Vercel deployment"""
    try:
        # Run migrations
        call_command('migrate', verbosity=0)
        
        # Create superuser if doesn't exist
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email=config('ADMIN_EMAIL', default='admin@example.com'),
                password='admin123'
            )
            message = "✅ Database setup complete! Superuser created: admin/admin123"
        else:
            message = "✅ Database migrations complete! Superuser already exists."
            
        return JsonResponse({
            'status': 'success',
            'message': message
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error', 
            'message': f'Setup failed: {str(e)}'
        })

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include('accounts.urls')),
    path("logs/", include('logs.urls')),
    path("adminpanel/", include('adminpanel.urls')),
    path("user/", include('userpanel.urls')),
    path("setup-db/", setup_database_view, name='setup_database'),
    # Landing page commented - direct to login
    # path("", include('public.urls')),
    path("", lambda request: redirect('/accounts/login/')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

