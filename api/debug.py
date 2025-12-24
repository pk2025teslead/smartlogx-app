from django.http import JsonResponse
import sys
import os

def handler(request):
    try:
        # Check Python path
        python_path = sys.path
        
        # Check if Django can be imported
        import django
        django_version = django.get_version()
        
        # Check environment variables
        database_url = os.environ.get('DATABASE_URL', 'Not set')
        secret_key = os.environ.get('SECRET_KEY', 'Not set')
        
        return JsonResponse({
            'status': 'success',
            'python_version': sys.version,
            'django_version': django_version,
            'database_url_set': 'Yes' if database_url != 'Not set' else 'No',
            'secret_key_set': 'Yes' if secret_key != 'Not set' else 'No',
            'python_path_count': len(python_path)
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'error_type': type(e).__name__
        })