#!/usr/bin/env python
"""
Simple test for database connection
"""
import os
import django
from decouple import config

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_production')

try:
    django.setup()
    from django.db import connection
    
    print("🔄 Testing database connection...")
    print(f"Database URL: {config('DATABASE_URL')[:50]}...")
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT version()")
        result = cursor.fetchone()
        print(f"✅ Connected to PostgreSQL: {result[0]}")
        
    print("✅ Database connection successful!")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\n💡 Make sure your DATABASE_URL in .env is correct")