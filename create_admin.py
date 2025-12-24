#!/usr/bin/env python
"""
Complete database setup for SmartLogX with SQLite
Creates admin user and sample data
"""
import os
import django
from datetime import datetime, date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartlogx.settings')
django.setup()

from django.contrib.auth.models import User
from logs.models import Log

def create_admin_user():
    """Create default admin user if it doesn't exist"""
    try:
        if not User.objects.filter(is_superuser=True).exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@smartlogx.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            print("✅ Admin user created!")
            print("Username: admin")
            print("Password: admin123")
            print("⚠️  Please change this password after first login!")
            return admin_user
        else:
            admin_user = User.objects.filter(is_superuser=True).first()
            print("✅ Admin user already exists")
            return admin_user
            
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return None

def create_sample_users():
    """Create sample users for testing"""
    sample_users = [
        {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
        {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
        {'username': 'mike_wilson', 'email': 'mike@example.com', 'first_name': 'Mike', 'last_name': 'Wilson'},
    ]
    
    created_users = []
    for user_data in sample_users:
        try:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password='password123',
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name']
                )
                created_users.append(user)
                print(f"✅ Created user: {user.username}")
            else:
                user = User.objects.get(username=user_data['username'])
                created_users.append(user)
                print(f"✅ User already exists: {user.username}")
        except Exception as e:
            print(f"❌ Error creating user {user_data['username']}: {e}")
    
    return created_users

def create_sample_logs():
    """Create sample logs for testing"""
    users = User.objects.all()
    if not users:
        print("❌ No users found to create logs")
        return
    
    sample_logs = [
        {
            'title': 'Project Kickoff Meeting',
            'description': 'Attended project kickoff meeting with the development team. Discussed project scope, timeline, and deliverables.',
            'priority': 'High',
            'log_date': date(2024, 12, 20)
        },
        {
            'title': 'Database Schema Design',
            'description': 'Completed the database schema design for the SmartLogX application. Defined all necessary tables and relationships.',
            'priority': 'High',
            'log_date': date(2024, 12, 21)
        },
        {
            'title': 'UI/UX Research',
            'description': 'Conducted research on modern UI/UX trends. Decided to implement glassmorphism design for better user experience.',
            'priority': 'Medium',
            'log_date': date(2024, 12, 22)
        },
        {
            'title': 'Frontend Development',
            'description': 'Started frontend development using HTML, CSS, and JavaScript. Implemented responsive design principles.',
            'priority': 'High',
            'log_date': date(2024, 12, 23)
        },
        {
            'title': 'Backend API Development',
            'description': 'Developed REST APIs for user authentication, log management, and data retrieval.',
            'priority': 'High',
            'log_date': date(2024, 12, 24)
        },
        {
            'title': 'Code Review',
            'description': 'Conducted code review session with team members. Fixed several bugs and improved code quality.',
            'priority': 'Medium',
            'log_date': date(2024, 12, 24)
        },
        {
            'title': 'Testing and Debugging',
            'description': 'Performed comprehensive testing of all features. Fixed critical bugs and improved performance.',
            'priority': 'High',
            'log_date': date(2024, 12, 24)
        },
        {
            'title': 'Documentation Update',
            'description': 'Updated project documentation including API documentation and user manual.',
            'priority': 'Low',
            'log_date': date(2024, 12, 24)
        }
    ]
    
    created_logs = 0
    for user in users:
        for log_data in sample_logs:
            try:
                # Check if log already exists
                if not Log.objects.filter(
                    user=user, 
                    title=log_data['title'], 
                    log_date=log_data['log_date']
                ).exists():
                    log = Log.objects.create(
                        user=user,
                        title=log_data['title'],
                        description=log_data['description'],
                        priority=log_data['priority'],
                        log_date=log_data['log_date']
                    )
                    created_logs += 1
            except Exception as e:
                print(f"❌ Error creating log for {user.username}: {e}")
    
    print(f"✅ Created {created_logs} sample logs")

def setup_complete_database():
    """Complete database setup"""
    print("🚀 Setting up SmartLogX database...")
    
    # Create admin user
    admin_user = create_admin_user()
    
    # Create sample users
    print("\n👥 Creating sample users...")
    sample_users = create_sample_users()
    
    # Create sample logs
    print("\n📝 Creating sample logs...")
    create_sample_logs()
    
    print("\n🎉 Database setup completed successfully!")
    print("\n📊 Database Summary:")
    print(f"   - Total Users: {User.objects.count()}")
    print(f"   - Total Logs: {Log.objects.count()}")
    print(f"   - Admin Users: {User.objects.filter(is_superuser=True).count()}")
    
    print("\n🔐 Login Credentials:")
    print("   Admin: admin / admin123")
    print("   Users: john_doe, jane_smith, mike_wilson / password123")
    print("\n⚠️  Please change default passwords after first login!")

if __name__ == '__main__':
    setup_complete_database()