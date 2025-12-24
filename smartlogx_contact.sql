-- SmartLogX Contact Inquiries Table
-- Run this SQL to create the contact form table

USE smartlogx_db;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
