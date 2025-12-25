-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: smartlogx_db
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts_userprofile`
--

DROP TABLE IF EXISTS `accounts_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_userprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_userprofile_user_id_92240672_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_userprofile`
--

LOCK TABLES `accounts_userprofile` WRITE;
/*!40000 ALTER TABLE `accounts_userprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_userprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `approval_codes`
--

DROP TABLE IF EXISTS `approval_codes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `approval_codes` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `USER_ID` int NOT NULL,
  `CODE` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `SESSION_TYPE` enum('First Half','Second Half') COLLATE utf8mb4_unicode_ci NOT NULL,
  `CREATED_AT` datetime DEFAULT CURRENT_TIMESTAMP,
  `EXPIRES_AT` datetime NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `idx_user_code` (`USER_ID`,`CODE`),
  KEY `idx_expires` (`EXPIRES_AT`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `approval_codes`
--

LOCK TABLES `approval_codes` WRITE;
/*!40000 ALTER TABLE `approval_codes` DISABLE KEYS */;
/*!40000 ALTER TABLE `approval_codes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendance_compoff`
--

DROP TABLE IF EXISTS `attendance_compoff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance_compoff` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `USER_ID` int NOT NULL,
  `SUNDAY_DATE` date NOT NULL,
  `WORK_PURPOSE` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `COMPOFF_DATE` date DEFAULT NULL,
  `NO_COMPOFF` tinyint(1) DEFAULT '0',
  `NOTES` text COLLATE utf8mb4_unicode_ci,
  `IS_APPROVED` tinyint(1) DEFAULT NULL,
  `APPROVER_ID` int DEFAULT NULL,
  `REQUESTED_AT` datetime DEFAULT CURRENT_TIMESTAMP,
  `APPROVED_AT` datetime DEFAULT NULL,
  `APPROVAL_NOTES` text COLLATE utf8mb4_unicode_ci,
  `CREATED_AT` datetime DEFAULT CURRENT_TIMESTAMP,
  `UPDATED_AT` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `idx_user_id` (`USER_ID`),
  KEY `idx_sunday_date` (`SUNDAY_DATE`),
  KEY `idx_is_approved` (`IS_APPROVED`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance_compoff`
--

LOCK TABLES `attendance_compoff` WRITE;
/*!40000 ALTER TABLE `attendance_compoff` DISABLE KEYS */;
/*!40000 ALTER TABLE `attendance_compoff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendance_leave`
--

DROP TABLE IF EXISTS `attendance_leave`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance_leave` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `USER_ID` int NOT NULL,
  `LEAVE_DATE` date NOT NULL,
  `LEAVE_TYPE` enum('Planned','Casual','Emergency','Sick') COLLATE utf8mb4_unicode_ci NOT NULL,
  `NOTES` text COLLATE utf8mb4_unicode_ci,
  `IS_APPROVED` tinyint(1) DEFAULT NULL,
  `APPROVER_ID` int DEFAULT NULL,
  `REQUESTED_AT` datetime DEFAULT CURRENT_TIMESTAMP,
  `APPROVED_AT` datetime DEFAULT NULL,
  `APPROVAL_NOTES` text COLLATE utf8mb4_unicode_ci,
  `CREATED_AT` datetime DEFAULT CURRENT_TIMESTAMP,
  `UPDATED_AT` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `idx_user_id` (`USER_ID`),
  KEY `idx_leave_date` (`LEAVE_DATE`),
  KEY `idx_is_approved` (`IS_APPROVED`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance_leave`
--

LOCK TABLES `attendance_leave` WRITE;
/*!40000 ALTER TABLE `attendance_leave` DISABLE KEYS */;
INSERT INTO `attendance_leave` VALUES (1,1,'2025-11-28','Casual','56445654654',1,1,'2025-11-28 23:58:05','2025-11-29 10:06:57','','2025-11-28 23:58:05','2025-11-29 10:06:57'),(2,1,'2025-11-29','Casual','Some personal work',1,1,'2025-11-29 11:13:13','2025-11-29 11:25:58','ok','2025-11-29 11:13:13','2025-11-29 11:25:58'),(3,1,'2025-11-29','Planned','i planned leave for 2 days',1,1,'2025-11-29 17:28:11','2025-11-29 17:29:03','proceed','2025-11-29 17:28:11','2025-11-29 17:29:03');
/*!40000 ALTER TABLE `attendance_leave` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendance_leave_audit`
--

DROP TABLE IF EXISTS `attendance_leave_audit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance_leave_audit` (
  `id` int NOT NULL AUTO_INCREMENT,
  `leave_id` int NOT NULL,
  `action` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'CREATED / EDITED / APPROVED / REJECTED / CANCELLED / DELETED',
  `actor_id` int NOT NULL COMMENT 'User who performed the action',
  `actor_role` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'USER / ADMIN',
  `actor_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Cached actor name for display',
  `old_data` json DEFAULT NULL COMMENT 'Previous values before change',
  `new_data` json DEFAULT NULL COMMENT 'New values after change',
  `reason` text COLLATE utf8mb4_unicode_ci COMMENT 'Reason for action (e.g., rejection reason)',
  `ip_address` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'IP address of actor',
  `user_agent` text COLLATE utf8mb4_unicode_ci COMMENT 'Browser user agent',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_leave_id` (`leave_id`),
  KEY `idx_actor_id` (`actor_id`),
  KEY `idx_action` (`action`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `fk_audit_leave` FOREIGN KEY (`leave_id`) REFERENCES `attendance_leave_v2` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance_leave_audit`
--

LOCK TABLES `attendance_leave_audit` WRITE;
/*!40000 ALTER TABLE `attendance_leave_audit` DISABLE KEYS */;
/*!40000 ALTER TABLE `attendance_leave_audit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendance_leave_v2`
--

DROP TABLE IF EXISTS `attendance_leave_v2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance_leave_v2` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `leave_date` date NOT NULL,
  `leave_type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'PLANNED / CASUAL / EMERGENCY / SICK',
  `notes` text COLLATE utf8mb4_unicode_ci,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'PENDING' COMMENT 'PENDING / APPROVED / REJECTED / CANCELLED',
  `is_editable` tinyint(1) NOT NULL DEFAULT '1' COMMENT 'Convenience flag for edit window',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `editable_until` datetime NOT NULL COMMENT 'created_at + 10 minutes',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` int NOT NULL COMMENT 'User who created the request',
  `approved_by` int DEFAULT NULL COMMENT 'Admin who approved/rejected',
  `approved_at` datetime DEFAULT NULL,
  `approval_notes` text COLLATE utf8mb4_unicode_ci COMMENT 'Admin notes for approval/rejection',
  `email_sent_admin` tinyint(1) DEFAULT '0' COMMENT 'Email sent to admin on create',
  `email_sent_user` tinyint(1) DEFAULT '0' COMMENT 'Email sent to user on approve/reject',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`),
  KEY `idx_leave_date` (`leave_date`),
  KEY `idx_created_at` (`created_at`),
  KEY `idx_editable_until` (`editable_until`),
  KEY `fk_leave_creator` (`created_by`),
  CONSTRAINT `fk_leave_creator` FOREIGN KEY (`created_by`) REFERENCES `users_master` (`ID`) ON DELETE CASCADE,
  CONSTRAINT `fk_leave_user` FOREIGN KEY (`user_id`) REFERENCES `users_master` (`ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance_leave_v2`
--

LOCK TABLES `attendance_leave_v2` WRITE;
/*!40000 ALTER TABLE `attendance_leave_v2` DISABLE KEYS */;
INSERT INTO `attendance_leave_v2` VALUES (1,1,'2025-11-28','Casual','56445654654','APPROVED',0,'2025-11-28 23:58:05','2025-11-29 00:08:05','2025-11-29 10:06:57',1,1,'2025-11-29 10:06:57','',0,0),(2,1,'2025-11-29','Casual','Some personal work','APPROVED',0,'2025-11-29 11:13:13','2025-11-29 11:23:13','2025-11-29 11:25:58',1,1,'2025-11-29 11:25:58','ok',0,0),(3,1,'2025-11-29','Planned','i planned leave for 2 days','APPROVED',0,'2025-11-29 17:28:11','2025-11-29 17:38:11','2025-11-29 17:29:03',1,1,'2025-11-29 17:29:03','proceed',0,0);
/*!40000 ALTER TABLE `attendance_leave_v2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendance_wfh`
--

DROP TABLE IF EXISTS `attendance_wfh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance_wfh` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `USER_ID` int NOT NULL,
  `WFH_DATE` date NOT NULL,
  `REASON` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `NOTES` text COLLATE utf8mb4_unicode_ci,
  `IS_APPROVED` tinyint(1) DEFAULT NULL,
  `APPROVER_ID` int DEFAULT NULL,
  `REQUESTED_AT` datetime DEFAULT CURRENT_TIMESTAMP,
  `APPROVED_AT` datetime DEFAULT NULL,
  `APPROVAL_NOTES` text COLLATE utf8mb4_unicode_ci,
  `CREATED_AT` datetime DEFAULT CURRENT_TIMESTAMP,
  `UPDATED_AT` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `idx_user_id` (`USER_ID`),
  KEY `idx_wfh_date` (`WFH_DATE`),
  KEY `idx_is_approved` (`IS_APPROVED`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance_wfh`
--

LOCK TABLES `attendance_wfh` WRITE;
/*!40000 ALTER TABLE `attendance_wfh` DISABLE KEYS */;
/*!40000 ALTER TABLE `attendance_wfh` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add user profile',7,'add_userprofile'),(26,'Can change user profile',7,'change_userprofile'),(27,'Can delete user profile',7,'delete_userprofile'),(28,'Can view user profile',7,'view_userprofile'),(29,'Can add log',8,'add_log'),(30,'Can change log',8,'change_log'),(31,'Can delete log',8,'delete_log'),(32,'Can view log',8,'view_log');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$xLbYNg3nQHvQw2aMlY6wXc$RpId9bHYXqUHdX2s9wF2/LsPqXd1SRzedHUWMpr497Q=','2025-12-24 07:24:40.249993',1,'admin','PANDI KUMAR','P','pandikumar652001@gmail.com',1,1,'2025-11-28 15:10:53.217616');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact_inquiries`
--

DROP TABLE IF EXISTS `contact_inquiries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact_inquiries` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `NAME` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `EMAIL` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `COMPANY` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `MESSAGE` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `IS_READ` tinyint(1) DEFAULT '0',
  `CREATED_AT` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `idx_email` (`EMAIL`),
  KEY `idx_created` (`CREATED_AT`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact_inquiries`
--

LOCK TABLES `contact_inquiries` WRITE;
/*!40000 ALTER TABLE `contact_inquiries` DISABLE KEYS */;
/*!40000 ALTER TABLE `contact_inquiries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (7,'accounts','userprofile'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(8,'logs','log'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-11-28 15:10:04.681908'),(2,'auth','0001_initial','2025-11-28 15:10:06.082605'),(3,'accounts','0001_initial','2025-11-28 15:10:06.299018'),(4,'admin','0001_initial','2025-11-28 15:10:06.649440'),(5,'admin','0002_logentry_remove_auto_add','2025-11-28 15:10:06.668281'),(6,'admin','0003_logentry_add_action_flag_choices','2025-11-28 15:10:06.686215'),(7,'contenttypes','0002_remove_content_type_name','2025-11-28 15:10:06.983062'),(8,'auth','0002_alter_permission_name_max_length','2025-11-28 15:10:07.139722'),(9,'auth','0003_alter_user_email_max_length','2025-11-28 15:10:07.203021'),(10,'auth','0004_alter_user_username_opts','2025-11-28 15:10:07.223530'),(11,'auth','0005_alter_user_last_login_null','2025-11-28 15:10:07.374878'),(12,'auth','0006_require_contenttypes_0002','2025-11-28 15:10:07.382405'),(13,'auth','0007_alter_validators_add_error_messages','2025-11-28 15:10:07.398925'),(14,'auth','0008_alter_user_username_max_length','2025-11-28 15:10:07.568496'),(15,'auth','0009_alter_user_last_name_max_length','2025-11-28 15:10:07.737001'),(16,'auth','0010_alter_group_name_max_length','2025-11-28 15:10:07.787737'),(17,'auth','0011_update_proxy_permissions','2025-11-28 15:10:07.803579'),(18,'auth','0012_alter_user_first_name_max_length','2025-11-28 15:10:07.986335'),(19,'logs','0001_initial','2025-11-28 15:10:08.179145'),(20,'sessions','0001_initial','2025-11-28 15:10:08.262409');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('la3ggbf95xicqt2l2l5689z770eb42xs','.eJxVjEEOwiAQAP_C2RBYqO169O4bCOwuUjU0Ke3J-HdD0oNeZybzViHuWwl7kzXMrC7KqtMvS5GeUrvgR6z3RdNSt3VOuif6sE3fFpbX9Wj_BiW20reEBixIctkSZ7T-DGZgmtjQSDxGpMTAjiShmIzgGKOf2DsPfoCkPl_1ojhT:1vQLhw:71HyLaNkSKC6EiUcMGwoHxl7cyAs6IwihWuFiQ-M3pg','2025-12-16 08:26:00.241607'),('lcbrg434n0fy7qyvaa8ft9z81x3h3f7e','.eJyrViotTi2Kz00sLgFSmSlKVoY6KEJ5ibmpSlZKXvkZeQouqWWpOfkFqUVKqGqK8nNAaoL93ULCHYNcFVxcw1x9_ANcg5RqAZBlIUU:1vPJcl:ZDOn4gfqfAChuabpTNH6SQTXiHxQ2pwHml5aLld0u-k','2025-12-13 12:00:23.487633'),('lfunx0kzb4l6yipn1zt271rw5bsn3a9s','.eJxVjEEKwyAQAP_iuUjjatUee-8bRHfXxDYoxORU-vcSCJRcZ4b5iFyWvoa5jaWGrfMSCom7uogQt3X6EzGIE0sR31x3Qa9Yxyax1XUpSe6JPGyXz0Y8P472NJhin_atsxYIfSTAxFYpipoh5QwJkbK_sctoAZTxWmk9-AzaXc3gAdhYZ8T3B1NVQIA:1vYJEe:4cQLJ_9nw6ki2wlfnhFsUGoBRN0zE2PyDqDeaA9Jgbs','2026-01-07 07:24:40.255128');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logs_log`
--

DROP TABLE IF EXISTS `logs_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logs_log` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `priority` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `log_date` date NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `logs_log_user_id_f24e8690_fk_auth_user_id` (`user_id`),
  CONSTRAINT `logs_log_user_id_f24e8690_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs_log`
--

LOCK TABLES `logs_log` WRITE;
/*!40000 ALTER TABLE `logs_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `logs_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `PROJECT_NAME` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `PROJECT_CODE` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `DESCRIPTION` text COLLATE utf8mb4_unicode_ci,
  `IS_ACTIVE` tinyint(1) DEFAULT '1',
  `CREATED_AT` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `PROJECT_CODE` (`PROJECT_CODE`),
  KEY `idx_active` (`IS_ACTIVE`),
  KEY `idx_name` (`PROJECT_NAME`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects`
--

LOCK TABLES `projects` WRITE;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` VALUES (1,'SmartLogX Development','SLX-DEV','Main SmartLogX application development',1,'2025-11-28 22:18:14'),(2,'Client Portal','CP-001','Client facing portal development',1,'2025-11-28 22:18:14'),(3,'Internal Tools','INT-TOOLS','Internal productivity tools',1,'2025-11-28 22:18:14'),(4,'Mobile App','MOB-APP','Mobile application development',1,'2025-11-28 22:18:14'),(5,'API Development','API-DEV','Backend API development',1,'2025-11-28 22:18:14'),(6,'UI/UX Design','UI-UX','User interface and experience design',1,'2025-11-28 22:18:14'),(7,'Testing & QA','TEST-QA','Quality assurance and testing',1,'2025-11-28 22:18:14'),(8,'Documentation','DOCS','Technical documentation',1,'2025-11-28 22:18:14');
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_column_preferences`
--

DROP TABLE IF EXISTS `user_column_preferences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_column_preferences` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `USER_ID` int NOT NULL,
  `TABLE_NAME` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `COLUMN_ORDER` json NOT NULL,
  `CREATED_AT` datetime DEFAULT CURRENT_TIMESTAMP,
  `UPDATED_AT` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `unique_user_table` (`USER_ID`,`TABLE_NAME`),
  KEY `idx_user_id` (`USER_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_column_preferences`
--

LOCK TABLES `user_column_preferences` WRITE;
/*!40000 ALTER TABLE `user_column_preferences` DISABLE KEYS */;
INSERT INTO `user_column_preferences` VALUES (1,1,'leave','[\"sno\", \"date\", \"notes\", \"type\", \"status\", \"action\"]','2025-11-28 23:58:10','2025-11-28 23:58:10'),(2,6,'logs','[\"sno\", \"date\", \"project\", \"heading\", \"session\", \"action\"]','2025-11-29 11:23:51','2025-11-29 11:24:11'),(5,1,'compoff','[\"sno\", \"sunday_date\", \"compoff_date\", \"work_purpose\", \"status\", \"action\"]','2025-12-02 12:13:09','2025-12-02 12:13:09');
/*!40000 ALTER TABLE `user_column_preferences` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_logs`
--

DROP TABLE IF EXISTS `user_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_logs` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `USER_ID` int NOT NULL,
  `PROJECT_TITLE` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `LOG_HEADING` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `LOG_DETAILS` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `LOG_DATE` date NOT NULL,
  `SESSION_TYPE` enum('First Half','Second Half') COLLATE utf8mb4_unicode_ci NOT NULL,
  `APPROVAL_REQUIRED` tinyint(1) DEFAULT '0',
  `APPROVAL_CODE` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `CREATED_AT` datetime DEFAULT CURRENT_TIMESTAMP,
  `UPDATED_AT` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `idx_user_id` (`USER_ID`),
  KEY `idx_log_date` (`LOG_DATE`),
  KEY `idx_session` (`SESSION_TYPE`),
  KEY `idx_user_date` (`USER_ID`,`LOG_DATE`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_logs`
--

LOCK TABLES `user_logs` WRITE;
/*!40000 ALTER TABLE `user_logs` DISABLE KEYS */;
INSERT INTO `user_logs` VALUES (1,1,'SAFETY VALVE SYSTEM','SUPPORT ONLINE','SUPPORT THORUGH TEAM VIWER','2025-11-28','First Half',1,'594293','2025-11-28 22:20:50','2025-11-28 22:20:50'),(2,6,'SAFETY VALVE SYSTEM','TESTING FOR ONLINE','THE EXAMPLE OF TESTING','2025-11-29','First Half',1,'120236','2025-11-29 11:20:00','2025-11-29 11:20:00'),(3,1,'SAFETY VALVE SYSTEM','SUPPORT ONLINE','THE DETAIL SHOULD BE PROVIDE THE LOG DETAILS','2025-12-02','First Half',0,NULL,'2025-12-02 13:41:22','2025-12-02 13:41:22');
/*!40000 ALTER TABLE `user_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_master`
--

DROP TABLE IF EXISTS `users_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_master` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `EMP_ID` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `EMP_NAME` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `MOBILE_NUMBER` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `EMAIL` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ROLE` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ROLL` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `PASSWORD` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `IS_FIRST_LOGIN` tinyint(1) DEFAULT '1',
  `CREATED_AT` datetime DEFAULT CURRENT_TIMESTAMP,
  `UPDATED_AT` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `EMP_ID` (`EMP_ID`),
  UNIQUE KEY `EMAIL` (`EMAIL`),
  KEY `idx_emp_id` (`EMP_ID`),
  KEY `idx_email` (`EMAIL`),
  KEY `idx_role` (`ROLE`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_master`
--

LOCK TABLES `users_master` WRITE;
/*!40000 ALTER TABLE `users_master` DISABLE KEYS */;
INSERT INTO `users_master` VALUES (1,'EMP001','John Developer','9876543210','john.dev@smartlogx.com','SOFTWARE DEVELOPER','Backend Team','pbkdf2_sha256$720000$XWBOr4Fbw29qaBjm6ROtmo$qHVNscTMe+J0bLyAWj4Afz8DJ7x2u8vErqRZx/7uY9c=',0,'2025-11-28 21:05:04','2025-11-28 21:56:09'),(2,'EMP002','Jane Tester','9876543211','jane.test@smartlogx.com','SOFTWARE TESTER','QA Team','pbkdf2_sha256$720000$UXPqsJ3lGZgSkW64oUd0E2$Bft3M35jSrjstZisyCqmvpKfwJ/J53xa6REXs0YUaiI=',1,'2025-11-28 21:05:04','2025-11-28 21:05:04'),(3,'EMP003','Mike Designer','9876543212','mike.design@smartlogx.com','UI UX DESIGNER','Design Team','pbkdf2_sha256$720000$UXPqsJ3lGZgSkW64oUd0E2$Bft3M35jSrjstZisyCqmvpKfwJ/J53xa6REXs0YUaiI=',1,'2025-11-28 21:05:04','2025-11-28 21:05:04'),(4,'EMP004','Sarah Coordinator','9876543213','sarah.coord@smartlogx.com','IT COORDINATOR','IT Operations','pbkdf2_sha256$720000$UXPqsJ3lGZgSkW64oUd0E2$Bft3M35jSrjstZisyCqmvpKfwJ/J53xa6REXs0YUaiI=',1,'2025-11-28 21:05:04','2025-11-28 21:05:04'),(5,'EMP008','DHARANI','9876543210','dharaniteslead@gmail.com','SOFTWARE DEVELOPER','IT','pbkdf2_sha256$720000$DuBHIIyqpzv5nLVuLUZ5ex$wrtH3YpeyoMS5hbTHVFt5f9joiMoIbIgmuQvieLoBQ0=',1,'2025-11-29 10:40:06','2025-11-29 10:40:06'),(6,'10034','ARUN','9876541230','arunpandian@teslead.com','IT COORDINATOR','IT','pbkdf2_sha256$720000$pjSTo7bxVx41fNnpYw78o9$dud3xH4gwmrB2GuPKRW071y/evjFkdyOfaGByctT6ag=',0,'2025-11-29 11:16:35','2025-11-29 11:17:56');
/*!40000 ALTER TABLE `users_master` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `vw_leave_details`
--

DROP TABLE IF EXISTS `vw_leave_details`;
/*!50001 DROP VIEW IF EXISTS `vw_leave_details`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_leave_details` AS SELECT 
 1 AS `id`,
 1 AS `user_id`,
 1 AS `leave_date`,
 1 AS `leave_type`,
 1 AS `notes`,
 1 AS `status`,
 1 AS `is_editable`,
 1 AS `created_at`,
 1 AS `editable_until`,
 1 AS `updated_at`,
 1 AS `created_by`,
 1 AS `approved_by`,
 1 AS `approved_at`,
 1 AS `approval_notes`,
 1 AS `email_sent_admin`,
 1 AS `email_sent_user`,
 1 AS `emp_id`,
 1 AS `emp_name`,
 1 AS `user_email`,
 1 AS `user_mobile`,
 1 AS `approver_name`,
 1 AS `edit_seconds_remaining`,
 1 AS `is_currently_editable`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `vw_leave_details`
--

/*!50001 DROP VIEW IF EXISTS `vw_leave_details`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_leave_details` AS select `l`.`id` AS `id`,`l`.`user_id` AS `user_id`,`l`.`leave_date` AS `leave_date`,`l`.`leave_type` AS `leave_type`,`l`.`notes` AS `notes`,`l`.`status` AS `status`,`l`.`is_editable` AS `is_editable`,`l`.`created_at` AS `created_at`,`l`.`editable_until` AS `editable_until`,`l`.`updated_at` AS `updated_at`,`l`.`created_by` AS `created_by`,`l`.`approved_by` AS `approved_by`,`l`.`approved_at` AS `approved_at`,`l`.`approval_notes` AS `approval_notes`,`l`.`email_sent_admin` AS `email_sent_admin`,`l`.`email_sent_user` AS `email_sent_user`,`u`.`EMP_ID` AS `emp_id`,`u`.`EMP_NAME` AS `emp_name`,`u`.`EMAIL` AS `user_email`,`u`.`MOBILE_NUMBER` AS `user_mobile`,`a`.`EMP_NAME` AS `approver_name`,greatest(0,timestampdiff(SECOND,now(),`l`.`editable_until`)) AS `edit_seconds_remaining`,(case when ((`l`.`status` = 'PENDING') and (now() <= `l`.`editable_until`)) then true else false end) AS `is_currently_editable` from ((`attendance_leave_v2` `l` join `users_master` `u` on((`l`.`user_id` = `u`.`ID`))) left join `users_master` `a` on((`l`.`approved_by` = `a`.`ID`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-25 14:20:17
