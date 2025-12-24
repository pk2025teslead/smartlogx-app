#!/usr/bin/env python
"""
SmartLogX - Change Admin Password Script
Run this script to change admin password easily
"""

import os
import sys
import django
import getpass

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartlogx.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


def change_admin_password():
    print("=" * 50)
    print("SmartLogX - Change Admin Password")
    print("=" * 50)
    print()
    
    # List existing superusers
    superusers = User.objects.filter(is_superuser=True)
    if not superusers.exists():
        print("❌ No admin users found!")
        print("Create one with: python manage.py createsuperuser")
        return
    
    print("Available admin users:")
    for i, user in enumerate(superusers, 1):
        print(f"{i}. {user.username} ({user.email})")
    
    print()
    
    # Select user
    if len(superusers) == 1:
        selected_user = superusers.first()
        print(f"Selected: {selected_user.username}")
    else:
        try:
            choice = int(input("Select user number: ")) - 1
            selected_user = superusers[choice]
        except (ValueError, IndexError):
            print("❌ Invalid selection")
            return
    
    print()
    
    # Get new password
    try:
        new_password = getpass.getpass("Enter new password: ")
        confirm_password = getpass.getpass("Confirm password: ")
    except KeyboardInterrupt:
        print("\n❌ Cancelled")
        return
    
    if not new_password:
        print("❌ Password cannot be empty")
        return
    
    if new_password != confirm_password:
        print("❌ Passwords don't match")
        return
    
    if len(new_password) < 6:
        print("❌ Password must be at least 6 characters")
        return
    
    # Update password
    try:
        selected_user.set_password(new_password)
        selected_user.save()
        print(f"✅ Password changed successfully for {selected_user.username}")
        print()
        print("You can now login with:")
        print(f"  Username: {selected_user.username}")
        print(f"  Password: [your new password]")
        print()
        print("Login URLs:")
        print("  - Admin Panel: http://127.0.0.1:8000/adminpanel/dashboard/")
        print("  - Django Admin: http://127.0.0.1:8000/admin/")
        
    except Exception as e:
        print(f"❌ Error changing password: {e}")


def change_employee_password():
    """Change password for users_master table users"""
    from django.db import connection
    from django.contrib.auth.hashers import make_password
    
    print("=" * 50)
    print("SmartLogX - Change Employee Password")
    print("=" * 50)
    print()
    
    # List employees
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ID, EMP_ID, EMP_NAME, EMAIL, ROLE
            FROM users_master
            ORDER BY EMP_ID
        """)
        employees = cursor.fetchall()
    
    if not employees:
        print("❌ No employees found!")
        print("Run: python setup_users_master.py")
        return
    
    print("Available employees:")
    for i, emp in enumerate(employees, 1):
        print(f"{i}. {emp[1]} - {emp[2]} ({emp[3]})")
    
    print()
    
    # Select employee
    try:
        choice = int(input("Select employee number: ")) - 1
        selected_emp = employees[choice]
    except (ValueError, IndexError):
        print("❌ Invalid selection")
        return
    
    print(f"Selected: {selected_emp[2]} ({selected_emp[1]})")
    print()
    
    # Get new password
    try:
        new_password = getpass.getpass("Enter new password: ")
        confirm_password = getpass.getpass("Confirm password: ")
    except KeyboardInterrupt:
        print("\n❌ Cancelled")
        return
    
    if not new_password:
        print("❌ Password cannot be empty")
        return
    
    if new_password != confirm_password:
        print("❌ Passwords don't match")
        return
    
    if len(new_password) < 6:
        print("❌ Password must be at least 6 characters")
        return
    
    # Update password
    try:
        hashed_password = make_password(new_password)
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE users_master 
                SET PASSWORD = %s, IS_FIRST_LOGIN = 0, UPDATED_AT = NOW()
                WHERE ID = %s
            """, [hashed_password, selected_emp[0]])
        
        print(f"✅ Password changed successfully for {selected_emp[2]}")
        print()
        print("Employee can now login with:")
        print(f"  Username: {selected_emp[1]} (or {selected_emp[3]})")
        print(f"  Password: [new password]")
        print()
        print("Login URL:")
        print("  - User Panel: http://127.0.0.1:8000/accounts/login/")
        
    except Exception as e:
        print(f"❌ Error changing password: {e}")


def main():
    print("Choose password change type:")
    print("1. Admin/Superuser password (Django admin)")
    print("2. Employee password (users_master table)")
    print()
    
    try:
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == "1":
            change_admin_password()
        elif choice == "2":
            change_employee_password()
        else:
            print("❌ Invalid choice")
    except KeyboardInterrupt:
        print("\n❌ Cancelled")


if __name__ == "__main__":
    main()