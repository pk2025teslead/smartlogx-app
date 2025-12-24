#!/usr/bin/env python
"""
Deployment management script for Vercel
Run this after deployment to set up your database
"""
import os
import django
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartlogx.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth.models import User

def setup_database():
    """Set up database for production"""
    print("🚀 Setting up database for production...")
    
    try:
        # Run migrations
        print("📦 Running migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations completed")
        
        # Create superuser if it doesn't exist
        if not User.objects.filter(is_superuser=True).exists():
            print("👤 Creating superuser...")
            User.objects.create_superuser(
                username='admin',
                email=config('ADMIN_EMAIL', default='admin@example.com'),
                password='admin123'  # Change this!
            )
            print("✅ Superuser created (username: admin, password: admin123)")
            print("⚠️  IMPORTANT: Change the admin password after first login!")
        else:
            print("👤 Superuser already exists")
        
        print("🎉 Database setup completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")

if __name__ == '__main__':
    setup_database()