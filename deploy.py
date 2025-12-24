#!/usr/bin/env python
"""
Deployment script for SmartLogX
Run this after deploying to set up initial data
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartlogx.settings')
django.setup()

from django.core.management import execute_from_command_line

def deploy():
    """Run deployment tasks"""
    print("Running migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("Collecting static files...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    print("Creating superuser (if needed)...")
    # You can add superuser creation logic here
    
    print("Deployment complete!")

if __name__ == '__main__':
    deploy()