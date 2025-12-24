-- ============================================
-- SmartLogX Leave Management Module V3
-- With Date Range Support (From Date - To Date)
-- Timezone: Asia/Kolkata (IST)
-- ============================================

-- ============================================
-- 1. ALTER TABLE: Add date range columns
-- ============================================
-- Run this to add new columns to existing table
ALTER TABLE attendance_leave_v2 
    ADD COLUMN from_date DATE NULL AFTER leave_date,
    ADD COLUMN to_date DATE NULL AFTER from_date,
    ADD COLUMN total_days INT DEFAULT 1 AFTER to_date;

-- Update existing records: copy leave_date to from_date and to_date
UPDATE attendance_leave_v2 
SET from_date = leave_date, 
    to_date = leave_date, 
    total_days = 1 
WHERE from_date IS NULL;

-- Make from_date NOT NULL after migration
ALTER TABLE attendance_leave_v2 
    MODIFY COLUMN from_date DATE NOT NULL,
    MODIFY COLUMN to_date DATE NOT NULL;

-- Add index for date range queries
ALTER TABLE attendance_leave_v2 
    ADD INDEX idx_from_date (from_date),
    ADD INDEX idx_to_date (to_date);


-- ============================================
-- 2. UPDATE VIEW: Include date range fields
-- ============================================
CREATE OR REPLACE VIEW vw_leave_details AS
SELECT 
    l.id,
    l.user_id,
    l.leave_date,
    l.from_date,
    l.to_date,
    l.total_days,
    l.leave_type,
    l.notes,
    l.status,
    l.is_editable,
    l.created_at,
    l.editable_until,
    l.updated_at,
    l.created_by,
    l.approved_by,
    l.approved_at,
    l.approval_notes,
    l.email_sent_admin,
    l.email_sent_user,
    u.EMP_ID as emp_id,
    u.EMP_NAME as emp_name,
    u.EMAIL as user_email,
    u.MOBILE_NUMBER as user_mobile,
    a.EMP_NAME as approver_name,
    -- Computed: seconds remaining in edit window
    GREATEST(0, TIMESTAMPDIFF(SECOND, NOW(), l.editable_until)) as edit_seconds_remaining,
    -- Computed: is currently editable (real-time check)
    CASE 
        WHEN l.status = 'PENDING' AND NOW() <= l.editable_until THEN TRUE 
        ELSE FALSE 
    END as is_currently_editable
FROM attendance_leave_v2 l
JOIN users_master u ON l.user_id = u.ID
LEFT JOIN users_master a ON l.approved_by = a.ID;


-- ============================================
-- 3. FRESH TABLE (Alternative - for new setup)
-- ============================================
-- Use this if setting up fresh instead of ALTER

/*
CREATE TABLE IF NOT EXISTS attendance_leave_v2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    leave_date DATE NOT NULL COMMENT 'Legacy single date field',
    from_date DATE NOT NULL COMMENT 'Leave start date',
    to_date DATE NOT NULL COMMENT 'Leave end date',
    total_days INT NOT NULL DEFAULT 1 COMMENT 'Total leave days',
    leave_type VARCHAR(50) NOT NULL COMMENT 'PLANNED / CASUAL / EMERGENCY / SICK',
    notes TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING' COMMENT 'PENDING / APPROVED / REJECTED / CANCELLED',
    
    -- Edit window fields
    is_editable BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    editable_until DATETIME NOT NULL,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Creator and approver tracking
    created_by INT NOT NULL,
    approved_by INT NULL,
    approved_at DATETIME NULL,
    approval_notes TEXT NULL,
    
    -- Email tracking
    email_sent_admin BOOLEAN DEFAULT FALSE,
    email_sent_user BOOLEAN DEFAULT FALSE,
    
    -- Indexes
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_leave_date (leave_date),
    INDEX idx_from_date (from_date),
    INDEX idx_to_date (to_date),
    INDEX idx_created_at (created_at),
    
    CONSTRAINT fk_leave_user FOREIGN KEY (user_id) REFERENCES users_master(ID) ON DELETE CASCADE,
    CONSTRAINT fk_leave_creator FOREIGN KEY (created_by) REFERENCES users_master(ID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
*/
