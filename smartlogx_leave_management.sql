-- ============================================
-- SmartLogX Leave Management Module
-- Database Schema with Audit Trail
-- Timezone: Asia/Kolkata (IST)
-- ============================================

-- Drop existing tables if needed (comment out in production)
-- DROP TABLE IF EXISTS attendance_leave_audit;
-- DROP TABLE IF EXISTS attendance_leave_v2;

-- ============================================
-- 1. LEAVE TABLE (Enhanced with Edit Window)
-- ============================================
CREATE TABLE IF NOT EXISTS attendance_leave_v2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    leave_date DATE NOT NULL,
    leave_type VARCHAR(50) NOT NULL COMMENT 'PLANNED / CASUAL / EMERGENCY / SICK',
    notes TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING' COMMENT 'PENDING / APPROVED / REJECTED / CANCELLED',
    
    -- Edit window fields
    is_editable BOOLEAN NOT NULL DEFAULT TRUE COMMENT 'Convenience flag for edit window',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    editable_until DATETIME NOT NULL COMMENT 'created_at + 10 minutes',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Creator and approver tracking
    created_by INT NOT NULL COMMENT 'User who created the request',
    approved_by INT NULL COMMENT 'Admin who approved/rejected',
    approved_at DATETIME NULL,
    approval_notes TEXT NULL COMMENT 'Admin notes for approval/rejection',
    
    -- Email tracking
    email_sent_admin BOOLEAN DEFAULT FALSE COMMENT 'Email sent to admin on create',
    email_sent_user BOOLEAN DEFAULT FALSE COMMENT 'Email sent to user on approve/reject',
    
    -- Indexes
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_leave_date (leave_date),
    INDEX idx_created_at (created_at),
    INDEX idx_editable_until (editable_until),
    
    -- Foreign key (assuming users_master exists)
    CONSTRAINT fk_leave_user FOREIGN KEY (user_id) REFERENCES users_master(ID) ON DELETE CASCADE,
    CONSTRAINT fk_leave_creator FOREIGN KEY (created_by) REFERENCES users_master(ID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================
-- 2. LEAVE AUDIT TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS attendance_leave_audit (
    id INT AUTO_INCREMENT PRIMARY KEY,
    leave_id INT NOT NULL,
    action VARCHAR(50) NOT NULL COMMENT 'CREATED / EDITED / APPROVED / REJECTED / CANCELLED / DELETED',
    actor_id INT NOT NULL COMMENT 'User who performed the action',
    actor_role VARCHAR(50) NOT NULL COMMENT 'USER / ADMIN',
    actor_name VARCHAR(255) NULL COMMENT 'Cached actor name for display',
    
    -- Data snapshots (JSON)
    old_data JSON NULL COMMENT 'Previous values before change',
    new_data JSON NULL COMMENT 'New values after change',
    
    -- Additional context
    reason TEXT NULL COMMENT 'Reason for action (e.g., rejection reason)',
    ip_address VARCHAR(45) NULL COMMENT 'IP address of actor',
    user_agent TEXT NULL COMMENT 'Browser user agent',
    
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_leave_id (leave_id),
    INDEX idx_actor_id (actor_id),
    INDEX idx_action (action),
    INDEX idx_created_at (created_at),
    
    -- Foreign key
    CONSTRAINT fk_audit_leave FOREIGN KEY (leave_id) REFERENCES attendance_leave_v2(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================
-- 3. TRIGGERS FOR AUTOMATIC UPDATES
-- ============================================

-- Trigger to set editable_until on insert
DELIMITER //
CREATE TRIGGER IF NOT EXISTS trg_leave_before_insert
BEFORE INSERT ON attendance_leave_v2
FOR EACH ROW
BEGIN
    -- Set editable_until to created_at + 10 minutes
    IF NEW.editable_until IS NULL OR NEW.editable_until = '0000-00-00 00:00:00' THEN
        SET NEW.editable_until = DATE_ADD(NEW.created_at, INTERVAL 10 MINUTE);
    END IF;
    
    -- Set is_editable based on status
    IF NEW.status != 'PENDING' THEN
        SET NEW.is_editable = FALSE;
    END IF;
END//
DELIMITER ;

-- Trigger to update is_editable when status changes
DELIMITER //
CREATE TRIGGER IF NOT EXISTS trg_leave_before_update
BEFORE UPDATE ON attendance_leave_v2
FOR EACH ROW
BEGIN
    -- If status changed from PENDING, mark as not editable
    IF NEW.status != 'PENDING' THEN
        SET NEW.is_editable = FALSE;
    END IF;
END//
DELIMITER ;


-- ============================================
-- 4. STORED PROCEDURE: Check Edit Window
-- ============================================
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS sp_check_leave_editable(
    IN p_leave_id INT,
    IN p_user_id INT,
    OUT p_is_editable BOOLEAN,
    OUT p_message VARCHAR(255)
)
BEGIN
    DECLARE v_status VARCHAR(20);
    DECLARE v_owner_id INT;
    DECLARE v_editable_until DATETIME;
    DECLARE v_now DATETIME;
    
    SET v_now = CONVERT_TZ(NOW(), @@session.time_zone, 'Asia/Kolkata');
    
    SELECT status, user_id, editable_until
    INTO v_status, v_owner_id, v_editable_until
    FROM attendance_leave_v2
    WHERE id = p_leave_id;
    
    IF v_owner_id IS NULL THEN
        SET p_is_editable = FALSE;
        SET p_message = 'Leave request not found';
    ELSEIF v_owner_id != p_user_id THEN
        SET p_is_editable = FALSE;
        SET p_message = 'You are not authorized to edit this request';
    ELSEIF v_status != 'PENDING' THEN
        SET p_is_editable = FALSE;
        SET p_message = CONCAT('Cannot edit - status is ', v_status);
    ELSEIF v_now > v_editable_until THEN
        SET p_is_editable = FALSE;
        SET p_message = CONCAT('Edit window expired at ', DATE_FORMAT(v_editable_until, '%d-%b-%Y %H:%i IST'));
    ELSE
        SET p_is_editable = TRUE;
        SET p_message = 'Editable';
    END IF;
END//
DELIMITER ;


-- ============================================
-- 5. VIEW: Leave with User Details
-- ============================================
CREATE OR REPLACE VIEW vw_leave_details AS
SELECT 
    l.id,
    l.user_id,
    l.leave_date,
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
-- 6. SAMPLE DATA (Optional - for testing)
-- ============================================
-- INSERT INTO attendance_leave_v2 (user_id, leave_date, leave_type, notes, status, created_at, editable_until, created_by)
-- VALUES (1, CURDATE(), 'PLANNED', 'Test leave request', 'PENDING', NOW(), DATE_ADD(NOW(), INTERVAL 10 MINUTE), 1);


-- ============================================
-- 7. MIGRATION: Copy from old table (if needed)
-- ============================================
-- Run this to migrate data from attendance_leave to attendance_leave_v2
-- INSERT INTO attendance_leave_v2 (user_id, leave_date, leave_type, notes, status, created_at, editable_until, updated_at, created_by, approved_by, approved_at, approval_notes)
-- SELECT 
--     USER_ID, LEAVE_DATE, LEAVE_TYPE, NOTES, 
--     CASE WHEN IS_APPROVED = 1 THEN 'APPROVED' WHEN IS_APPROVED = 0 THEN 'REJECTED' ELSE 'PENDING' END,
--     COALESCE(REQUESTED_AT, CREATED_AT, NOW()),
--     DATE_ADD(COALESCE(REQUESTED_AT, CREATED_AT, NOW()), INTERVAL 10 MINUTE),
--     COALESCE(UPDATED_AT, NOW()),
--     USER_ID,
--     APPROVER_ID,
--     APPROVED_AT,
--     APPROVAL_NOTES
-- FROM attendance_leave;

