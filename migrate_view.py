# Add this to one of your views.py files
from django.http import JsonResponse
from django.core.management import call_command
from django.views.decorators.csrf import csrf_exempt
import os

@csrf_exempt
def run_migrations(request):
    """Run migrations via web endpoint (use once after deployment)"""
    if request.method == 'POST':
        try:
            call_command('migrate')
            return JsonResponse({'status': 'success', 'message': 'Migrations completed'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'POST method required'})