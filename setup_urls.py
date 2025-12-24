# Add this to your main urls.py or create a separate setup app
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
from django.contrib.auth.models import User
from decouple import config
import json

@csrf_exempt
def setup_database(request):
    """Setup database after deployment"""
    if request.method == 'POST':
        try:
            # Run migrations
            call_command('migrate')
            
            # Create superuser if needed
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(
                    username='admin',
                    email=config('ADMIN_EMAIL', default='admin@example.com'),
                    password='admin123'  # Change this!
                )
                return JsonResponse({
                    'status': 'success',
                    'message': 'Database setup completed. Superuser created (admin/admin123)',
                    'warning': 'Please change admin password immediately!'
                })
            else:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Database migrations completed. Superuser already exists.'
                })
                
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Setup failed: {str(e)}'
            })
    
    return JsonResponse({
        'status': 'info',
        'message': 'Send POST request to setup database'
    })