from django.db import models
from django.contrib.auth.models import User
from django.db import connection
from datetime import datetime

class Log(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logs')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Low')
    log_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'logs_log'
        ordering = ['-log_date', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    @staticmethod
    def create_log_raw(user_id, title, description, priority, log_date):
        """Raw SQL query to insert a new log"""
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO logs_log (user_id, title, description, priority, log_date, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
            """, [user_id, title, description, priority, log_date])
            return cursor.lastrowid

    @staticmethod
    def get_user_logs_raw(user_id):
        """Raw SQL query to fetch all logs for a user"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, user_id, title, description, priority, log_date, 
                       created_at, updated_at
                FROM logs_log
                WHERE user_id = %s
                ORDER BY log_date DESC, created_at DESC
            """, [user_id])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def get_log_by_id_raw(log_id, user_id=None):
        """Raw SQL query to fetch a specific log"""
        with connection.cursor() as cursor:
            if user_id:
                cursor.execute("""
                    SELECT id, user_id, title, description, priority, log_date, 
                           created_at, updated_at
                    FROM logs_log
                    WHERE id = %s AND user_id = %s
                """, [log_id, user_id])
            else:
                cursor.execute("""
                    SELECT id, user_id, title, description, priority, log_date, 
                           created_at, updated_at
                    FROM logs_log
                    WHERE id = %s
                """, [log_id])
            
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
        return None

    @staticmethod
    def update_log_raw(log_id, user_id, title, description, priority, log_date):
        """Raw SQL query to update a log"""
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE logs_log
                SET title = %s, description = %s, priority = %s, 
                    log_date = %s, updated_at = NOW()
                WHERE id = %s AND user_id = %s
            """, [title, description, priority, log_date, log_id, user_id])
            return cursor.rowcount > 0

    @staticmethod
    def delete_log_raw(log_id, user_id):
        """Raw SQL query to delete a log"""
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM logs_log
                WHERE id = %s AND user_id = %s
            """, [log_id, user_id])
            return cursor.rowcount > 0

    @staticmethod
    def get_all_logs_raw():
        """Raw SQL query to fetch all logs (for admin)"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT l.id, l.user_id, u.username, u.email, l.title, 
                       l.description, l.priority, l.log_date, 
                       l.created_at, l.updated_at
                FROM logs_log l
                INNER JOIN auth_user u ON l.user_id = u.id
                ORDER BY l.log_date DESC, l.created_at DESC
            """)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def get_logs_by_filter_raw(user_id=None, start_date=None, end_date=None, priority=None):
        """Raw SQL query to fetch filtered logs"""
        with connection.cursor() as cursor:
            query = """
                SELECT l.id, l.user_id, u.username, u.email, l.title, 
                       l.description, l.priority, l.log_date, 
                       l.created_at, l.updated_at
                FROM logs_log l
                INNER JOIN auth_user u ON l.user_id = u.id
                WHERE 1=1
            """
            params = []

            if user_id:
                query += " AND l.user_id = %s"
                params.append(user_id)
            
            if start_date:
                query += " AND l.log_date >= %s"
                params.append(start_date)
            
            if end_date:
                query += " AND l.log_date <= %s"
                params.append(end_date)
            
            if priority:
                query += " AND l.priority = %s"
                params.append(priority)

            query += " ORDER BY l.log_date DESC, l.created_at DESC"

            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def get_monthly_stats_raw(user_id):
        """Raw SQL query to get monthly log statistics"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    DATE_FORMAT(log_date, '%%Y-%%m') as month,
                    COUNT(*) as count,
                    SUM(CASE WHEN priority = 'High' THEN 1 ELSE 0 END) as high_priority,
                    SUM(CASE WHEN priority = 'Medium' THEN 1 ELSE 0 END) as medium_priority,
                    SUM(CASE WHEN priority = 'Low' THEN 1 ELSE 0 END) as low_priority
                FROM logs_log
                WHERE user_id = %s
                AND log_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
                GROUP BY DATE_FORMAT(log_date, '%%Y-%%m')
                ORDER BY month ASC
            """, [user_id])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def get_priority_stats_raw(user_id=None):
        """Raw SQL query to get priority-wise statistics"""
        with connection.cursor() as cursor:
            if user_id:
                cursor.execute("""
                    SELECT priority, COUNT(*) as count
                    FROM logs_log
                    WHERE user_id = %s
                    GROUP BY priority
                """, [user_id])
            else:
                cursor.execute("""
                    SELECT priority, COUNT(*) as count
                    FROM logs_log
                    GROUP BY priority
                """)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
