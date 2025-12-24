-- SmartLogX Database Schema
-- MySQL Database Setup

CREATE DATABASE IF NOT EXISTS smartlogx_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE smartlogx_db;

-- Users Table (Django auth_user will be used, but this is for reference)
-- Django will create auth_user table automatically

-- Logs Table
CREATE TABLE IF NOT EXISTS logs_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority ENUM('Low', 'Medium', 'High') DEFAULT 'Low',
    log_date DATE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_log_date (log_date),
    INDEX idx_priority (priority)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- User Profile Table (Extended user info)
CREATE TABLE IF NOT EXISTS accounts_userprofile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Sample Data for Testing
-- Note: You'll need to create users through Django admin first
-- Then you can insert sample logs

-- Example: Insert sample logs (replace user_id with actual user IDs)
-- INSERT INTO logs_log (user_id, title, description, priority, log_date) VALUES
-- (1, 'Project Kickoff', 'Started the SmartLogX project development', 'High', '2024-01-15'),
-- (1, 'Database Design', 'Completed database schema design', 'Medium', '2024-01-16'),
-- (1, 'UI Implementation', 'Implemented glassmorphism UI design', 'High', '2024-01-17');
