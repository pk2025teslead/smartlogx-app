-- ============================================
-- SmartLogX Attendance Management Schema
-- Leave, Comp-Off, WFH Tables
-- ============================================

USE smartlogx_db;

-- ============================================
-- 1. LEAVE INFORMATION TABLE
-- ============================================

DROP TABLE IF EXISTS attendance_leave;

CREATE TABLE attendance_leave (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    USER_ID INT NOT NULL COMMENT 'Reference to users_master.ID',
    LEAVE_DATE DATE NOT NULL COMMENT 'Date of leave',
    LEAVE_TYPE ENUM('Planned', 'Casual', 'Emergency', 'Sick') NOT NULL,
    NOTES TEXT COMMENT 'Additional notes',
    IS_APPROVED TINYINT(1) DEFAULT NULL COMMENT 'NULL=Pending, 0=Rejected, 1=Approved',
    APPROVER_ID INT DEFAULT NULL COMMENT 'Admin who approved/rejected',
    REQUESTED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
    APPROVED_AT DATETIME DEFAULT NULL,
    APPROVAL_NOTES TEXT COMMENT 'Admin notes on approval/rejection',
    CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
    UPDATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (USER_ID),
    INDEX idx_leave_date (LEAVE_DATE),
    INDEX idx_leave_type (LEAVE_TYPE),
    INDEX idx_is_approved (IS_APPROVED),
    INDEX idx_user_month (USER_ID, LEAVE_DATE)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================
-- 2. SUNDAY COMP-OFF TABLE
-- ============================================

DROP TABLE IF EXISTS attendance_compoff;

CREATE TABLE attendance_compoff (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    USER_ID INT NOT NULL COMMENT 'Reference to users_master.ID',
    SUNDAY_DATE DATE NOT NULL COMMENT 'Sunday worked date',
    WORK_PURPOSE VARCHAR(500) NOT NULL COMMENT 'Purpose of Sunday work',
    COMPOFF_DATE DATE DEFAULT NULL COMMENT 'Comp-off date taken (NULL if no comp-off)',
    NO_COMPOFF BOOLEAN DEFAULT 0 COMMENT 'True if user chose no comp-off',
    NOTES TEXT COMMENT 'Additional notes',
    IS_APPROVED TINYINT(1) DEFAULT NULL COMMENT 'NULL=Pending, 0=Rejected, 1=Approved',
    APPROVER_ID INT DEFAULT NULL,
    REQUESTED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
    APPROVED_AT DATETIME DEFAULT NULL,
    APPROVAL_NOTES TEXT,
    CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
    UPDATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (USER_ID),
    INDEX idx_sunday_date (SUNDAY_DATE),
    INDEX idx_compoff_date (COMPOFF_DATE),
    INDEX idx_is_approved (IS_APPROVED),
    INDEX idx_user_month (USER_ID, SUNDAY_DATE)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================
-- 3. WORK FROM HOME (WFH) TABLE
-- ============================================

DROP TABLE IF EXISTS attendance_wfh;

CREATE TABLE attendance_wfh (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    USER_ID INT NOT NULL COMMENT 'Reference to users_master.ID',
    WFH_DATE DATE NOT NULL COMMENT 'Work from home date',
    REASON VARCHAR(500) NOT NULL COMMENT 'Reason for WFH',
    NOTES TEXT COMMENT 'Additional notes',
    IS_APPROVED TINYINT(1) DEFAULT NULL COMMENT 'NULL=Pending, 0=Rejected, 1=Approved',
    APPROVER_ID INT DEFAULT NULL,
    REQUESTED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
    APPROVED_AT DATETIME DEFAULT NULL,
    APPROVAL_NOTES TEXT,
    CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
    UPDATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (USER_ID),
    INDEX idx_wfh_date (WFH_DATE),
    INDEX idx_is_approved (IS_APPROVED),
    INDEX idx_user_month (USER_ID, WFH_DATE)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================
-- 4. USER COLUMN PREFERENCES TABLE
-- ============================================

DROP TABLE IF EXISTS user_column_preferences;

CREATE TABLE user_column_preferences (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    USER_ID INT NOT NULL,
    TABLE_NAME VARCHAR(50) NOT NULL COMMENT 'Table identifier (logs, leave, compoff, wfh)',
    COLUMN_ORDER JSON NOT NULL COMMENT 'JSON array of column order',
    CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
    UPDATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_user_table (USER_ID, TABLE_NAME),
    INDEX idx_user_id (USER_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================
-- VIEWS FOR REPORTING
-- ============================================

-- Leave summary view
CREATE OR REPLACE VIEW v_leave_summary AS
SELECT 
    u.ID as USER_ID,
    u.EMP_NAME,
    YEAR(l.LEAVE_DATE) as YEAR,
    MONTH(l.LEAVE_DATE) as MONTH,
    COUNT(*) as TOTAL_LEAVES,
    SUM(CASE WHEN l.IS_APPROVED = 1 THEN 1 ELSE 0 END) as APPROVED_LEAVES,
    SUM(CASE WHEN l.IS_APPROVED = 0 THEN 1 ELSE 0 END) as REJECTED_LEAVES,
    SUM(CASE WHEN l.IS_APPROVED IS NULL THEN 1 ELSE 0 END) as PENDING_LEAVES
FROM users_master u
LEFT JOIN attendance_leave l ON u.ID = l.USER_ID
GROUP BY u.ID, u.EMP_NAME, YEAR(l.LEAVE_DATE), MONTH(l.LEAVE_DATE);
