from django.db import models
from django.contrib.auth.models import User
from django.db import connection

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'accounts_userprofile'

    def __str__(self):
        return f"{self.user.username} - Profile"

    @staticmethod
    def get_user_by_credentials_raw(username, password):
        """Raw SQL query to validate user credentials"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT u.id, u.username, u.password, u.is_staff, u.is_active, 
                       COALESCE(p.is_active, 1) as profile_active
                FROM auth_user u
                LEFT JOIN accounts_userprofile p ON u.id = p.user_id
                WHERE u.username = %s AND u.is_active = 1
            """, [username])
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'username': row[1],
                    'password': row[2],
                    'is_staff': row[3],
                    'is_active': row[4],
                    'profile_active': row[5]
                }
        return None

    @staticmethod
    def get_all_users_raw():
        """Raw SQL query to get all users with their profiles"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT u.id, u.username, u.email, u.first_name, u.last_name, 
                       u.is_staff, u.is_active, u.date_joined,
                       COALESCE(p.is_active, 1) as profile_active,
                       p.created_at
                FROM auth_user u
                LEFT JOIN accounts_userprofile p ON u.id = p.user_id
                ORDER BY u.date_joined DESC
            """)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def toggle_user_status_raw(user_id, status):
        """Raw SQL query to activate/deactivate user"""
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE accounts_userprofile 
                SET is_active = %s, updated_at = NOW()
                WHERE user_id = %s
            """, [status, user_id])
            
            cursor.execute("""
                UPDATE auth_user 
                SET is_active = %s
                WHERE id = %s
            """, [status, user_id])
