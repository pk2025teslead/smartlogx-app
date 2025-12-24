from django.core.wsgi import get_wsgi_application
import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartlogx.settings')

application = get_wsgi_application()

def handler(request):
    return application(request)