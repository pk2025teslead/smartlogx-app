#!/usr/bin/env python
"""
Debug database status
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartlogx.settings')
django.setup()

from django.contrib.auth.models import User
from logs.models import Log

def check_database():
    """Check database status"""
    try:
        print("🔍 Checking database status...")
        
        # Check if tables exist
        print(f"📊 Total Users: {User.objects.count()}")
        print(f"📊 Total Logs: {Log.objects.count()}")
        print(f"📊 Admin Users: {User.objects.filter(is_superuser=True).count()}")
        
        # List all users
        print("\n👥 All Users:")
        for user in User.objects.all():
            print(f"   - {user.username} ({'Admin' if user.is_superuser else 'User'}) - Active: {user.is_active}")
        
        # Check admin user specifically
        try:
            admin = User.objects.get(username='admin')
            print(f"\n🔐 Admin User Details:")
            print(f"   - Username: {admin.username}")
            print(f"   - Email: {admin.email}")
            print(f"   - Is Active: {admin.is_active}")
            print(f"   - Is Superuser: {admin.is_superuser}")
            print(f"   - Is Staff: {admin.is_staff}")
        except User.DoesNotExist:
            print("\n❌ Admin user not found!")
        
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == '__main__':
    check_database()