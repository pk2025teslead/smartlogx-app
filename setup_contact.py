"""
Setup script for SmartLogX Contact Inquiries table
Run this script to create the contact_inquiries table in MySQL
"""

import mysql.connector
from mysql.connector import Error

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'smartlogx_db'
}

def create_contact_table():
    """Create the contact_inquiries table"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Create contact_inquiries table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contact_inquiries (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                NAME VARCHAR(100) NOT NULL,
                EMAIL VARCHAR(150) NOT NULL,
                COMPANY VARCHAR(150),
                MESSAGE TEXT NOT NULL,
                IS_READ TINYINT(1) DEFAULT 0,
                CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_email (EMAIL),
                INDEX idx_created (CREATED_AT)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        connection.commit()
        print("✅ contact_inquiries table created successfully!")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("SmartLogX Contact Table Setup")
    print("=" * 50)
    create_contact_table()
    print("\n✅ Setup complete!")
