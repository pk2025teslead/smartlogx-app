#!/usr/bin/env python
"""
Test database connection before deployment
"""
import os
import django
from decouple import config

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartlogx.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line

def test_database():
    """Test database connection and run basic operations"""
    try:
        # Test connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"✅ Database connection successful: {result}")
        
        # Test migrations
        print("🔄 Running migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
        print("✅ Migrations completed successfully")
        
        # Test creating superuser (optional)
        print("👤 You can now create a superuser:")
        print("python manage.py createsuperuser")
        
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == '__main__':
    print("Testing Supabase database connection...")
    print(f"Database URL: {config('DATABASE_URL', default='Not set')[:50]}...")
    test_database()