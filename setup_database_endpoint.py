# Add this to your smartlogx/urls.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
from django.contrib.auth.models import User
from decouple import config
import json

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

# Add this URL pattern to your main urls.py:
# path('setup-db/', setup_database_view, name='setup_database'),