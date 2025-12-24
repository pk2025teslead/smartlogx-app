-- ============================================
-- SmartLogX Users Master Table
-- Zoho-style Admin Panel Database Schema
-- ============================================

-- Use the database
USE smartlogx_db;

-- Drop table if exists (for fresh setup)
DROP TABLE IF EXISTS users_master;

-- Create users_master table
CREATE TABLE users_master (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    EMP_ID VARCHAR(255) NOT NULL UNIQUE COMMENT 'Employee ID',
    EMP_NAME VARCHAR(255) NOT NULL COMMENT 'Employee Full Name',
    MOBILE_NUMBER VARCHAR(20) COMMENT 'Mobile Phone Number',
    EMAIL VARCHAR(255) NOT NULL UNIQUE COMMENT 'Email Address',
    ROLE VARCHAR(100) NOT NULL COMMENT 'Job Role',
    ROLL VARCHAR(255) COMMENT 'Department/Team',
    PASSWORD VARCHAR(255) NOT NULL COMMENT 'Hashed Password (PBKDF2)',
    IS_FIRST_LOGIN BOOLEAN DEFAULT 1 COMMENT 'Flag for first login password change',
    CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation timestamp',
    UPDATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Last update timestamp',
    
    -- Indexes for faster queries
    INDEX idx_emp_id (EMP_ID),
    INDEX idx_email (EMAIL),
    INDEX idx_role (ROLE),
    INDEX idx_created_at (CREATED_AT)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Sample Data (Optional)
-- Password for all sample users: Temp@123
-- Hash generated using Django's make_password()
-- ============================================

-- Note: The password hash below is a placeholder.
-- In production, use Django's make_password('Temp@123') to generate proper hash.
-- Example hash format: pbkdf2_sha256$600000$<salt>$<hash>

INSERT INTO users_master (EMP_ID, EMP_NAME, MOBILE_NUMBER, EMAIL, ROLE, ROLL, PASSWORD, IS_FIRST_LOGIN) VALUES
('EMP001', 'John Developer', '9876543210', 'john.dev@smartlogx.com', 'SOFTWARE DEVELOPER', 'Backend Team', 'pbkdf2_sha256$600000$placeholder$hash', 1),
('EMP002', 'Jane Tester', '9876543211', 'jane.test@smartlogx.com', 'SOFTWARE TESTER', 'QA Team', 'pbkdf2_sha256$600000$placeholder$hash', 1),
('EMP003', 'Mike Designer', '9876543212', 'mike.design@smartlogx.com', 'UI UX DESIGNER', 'Design Team', 'pbkdf2_sha256$600000$placeholder$hash', 1),
('EMP004', 'Sarah Coordinator', '9876543213', 'sarah.coord@smartlogx.com', 'IT COORDINATOR', 'IT Operations', 'pbkdf2_sha256$600000$placeholder$hash', 1);

-- ============================================
-- Useful Queries
-- ============================================

-- Get all users
-- SELECT * FROM users_master ORDER BY CREATED_AT DESC;

-- Get users by role
-- SELECT * FROM users_master WHERE ROLE = 'SOFTWARE DEVELOPER';

-- Get user count by role
-- SELECT ROLE, COUNT(*) as count FROM users_master GROUP BY ROLE;

-- Search users
-- SELECT * FROM users_master WHERE EMP_NAME LIKE '%search%' OR EMAIL LIKE '%search%';

-- Update password (use Django's make_password for hash)
-- UPDATE users_master SET PASSWORD = 'new_hash', IS_FIRST_LOGIN = 0, UPDATED_AT = NOW() WHERE ID = 1;

-- Reset password to Temp@123
-- UPDATE users_master SET PASSWORD = 'temp_hash', IS_FIRST_LOGIN = 1, UPDATED_AT = NOW() WHERE ID = 1;
