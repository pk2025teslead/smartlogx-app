#!/usr/bin/env python
"""
Test Supabase database connection
"""
import psycopg2
from decouple import config

def test_connection():
    try:
        # Test the connection string with correct password
        DATABASE_URL = "postgresql://postgres:Teslead202512@db.kgumbctnezsxiqlnke.supabase.co:5432/postgres"
        
        print("🔄 Testing Supabase connection...")
        print(f"URL: postgresql://postgres:***@db.kgumbctnezsxiqlnke.supabase.co:5432/postgres")
        
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        result = cursor.fetchone()
        
        print(f"✅ Connected successfully!")
        print(f"PostgreSQL version: {result[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == '__main__':
    test_connection()