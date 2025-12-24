-- ============================================
-- SmartLogX User Logs & Approval Codes Schema
-- For User Dashboard Log Management
-- ============================================

USE smartlogx_db;

-- ============================================
-- User Logs Table
-- ============================================

DROP TABLE IF EXISTS user_logs;

CREATE TABLE user_logs (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    USER_ID INT NOT NULL COMMENT 'Reference to users_master.ID',
    PROJECT_TITLE VARCHAR(255) NOT NULL COMMENT 'Project name/title',
    LOG_HEADING VARCHAR(255) NOT NULL COMMENT 'Log heading/summary',
    LOG_DETAILS TEXT NOT NULL COMMENT 'Detailed log content',
    LOG_DATE DATE NOT NULL COMMENT 'Date of the log entry',
    SESSION_TYPE ENUM('First Half', 'Second Half') NOT NULL COMMENT 'Session: First Half or Second Half',
    APPROVAL_REQUIRED BOOLEAN DEFAULT 0 COMMENT 'Was approval needed for this log',
    APPROVAL_CODE VARCHAR(10) NULL COMMENT 'Approval code used (if any)',
    CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
    UPDATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_user_id (USER_ID),
    INDEX idx_log_date (LOG_DATE),
    INDEX idx_session (SESSION_TYPE),
    INDEX idx_user_date (USER_ID, LOG_DATE),
    INDEX idx_year_month (USER_ID, LOG_DATE),
    
    -- Foreign Key (optional - uncomment if users_master exists)
    -- CONSTRAINT fk_user_logs_user FOREIGN KEY (USER_ID) REFERENCES users_master(ID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================
-- Approval Codes Table (Temporary Storage)
-- ============================================

DROP TABLE IF EXISTS approval_codes;

CREATE TABLE approval_codes (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    USER_ID INT NOT NULL COMMENT 'Reference to users_master.ID',
    CODE VARCHAR(10) NOT NULL COMMENT '6-digit approval code',
    SESSION_TYPE ENUM('First Half', 'Second Half') NOT NULL,
    CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
    EXPIRES_AT DATETIME NOT NULL COMMENT 'Code expiration time',
    
    -- Indexes
    INDEX idx_user_code (USER_ID, CODE),
    INDEX idx_expires (EXPIRES_AT)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================
-- Projects Table (Optional - for dropdown)
-- ============================================

DROP TABLE IF EXISTS projects;

CREATE TABLE projects (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    PROJECT_NAME VARCHAR(255) NOT NULL,
    PROJECT_CODE VARCHAR(50) UNIQUE,
    DESCRIPTION TEXT,
    IS_ACTIVE BOOLEAN DEFAULT 1,
    CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_active (IS_ACTIVE),
    INDEX idx_name (PROJECT_NAME)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Sample projects
INSERT INTO projects (PROJECT_NAME, PROJECT_CODE, DESCRIPTION, IS_ACTIVE) VALUES
('SmartLogX Development', 'SLX-DEV', 'Main SmartLogX application development', 1),
('Client Portal', 'CP-001', 'Client facing portal development', 1),
('Internal Tools', 'INT-TOOLS', 'Internal productivity tools', 1),
('Mobile App', 'MOB-APP', 'Mobile application development', 1),
('API Development', 'API-DEV', 'Backend API development', 1),
('UI/UX Design', 'UI-UX', 'User interface and experience design', 1),
('Testing & QA', 'TEST-QA', 'Quality assurance and testing', 1),
('Documentation', 'DOCS', 'Technical documentation', 1);


-- ============================================
-- Cleanup Job (Run periodically to remove expired codes)
-- ============================================

-- DELETE FROM approval_codes WHERE EXPIRES_AT < NOW();


-- ============================================
-- Sample Data for Testing
-- ============================================

-- Insert sample logs (assuming user ID 1 exists)
-- INSERT INTO user_logs (USER_ID, PROJECT_TITLE, LOG_HEADING, LOG_DETAILS, LOG_DATE, SESSION_TYPE, APPROVAL_REQUIRED) VALUES
-- (1, 'SmartLogX Development', 'Dashboard Implementation', 'Completed the user dashboard with Zoho-style dark theme. Implemented sidebar navigation and stats cards.', CURDATE(), 'First Half', 0),
-- (1, 'API Development', 'REST API Endpoints', 'Created CRUD endpoints for user management. Added authentication middleware.', CURDATE(), 'Second Half', 0);
