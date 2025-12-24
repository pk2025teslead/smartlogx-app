#!/usr/bin/env python
"""
Create default admin user for SmartLogX
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartlogx.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin():
    """Create default admin user if it doesn't exist"""
    try:
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@smartlogx.com',
                password='admin123'
            )
            print("✅ Admin user created!")
            print("Username: admin")
            print("Password: admin123")
            print("⚠️  Please change this password after first login!")
        else:
            print("✅ Admin user already exists")
            
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")

if __name__ == '__main__':
    create_admin()