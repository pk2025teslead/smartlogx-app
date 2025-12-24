import os
import sys
from django.core.wsgi import get_wsgi_application

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartlogx.settings')

app = get_wsgi_application()