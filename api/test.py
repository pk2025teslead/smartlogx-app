from django.http import JsonResponse
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartlogx.settings')

def handler(request):
    try:
        import django
        django.setup()
        return JsonResponse({
            'status': 'success',
            'message': 'Django is working on Vercel!',
            'django_version': django.get_version()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })