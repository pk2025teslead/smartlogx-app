"""
SmartLogX Leave Management Module - Unit Tests
Tests for server-side logic, edit window enforcement, and status transitions
"""

import pytest
import json
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client, TransactionTestCase
from django.db import connection
import pytz

# Import the module under test
from adminpanel import leave_models as models


IST = pytz.timezone('Asia/Kolkata')


class LeaveModelTestCase(TransactionTestCase):
    """Test cases for leave model functions"""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create test tables if they don't exist
        cls._create_test_tables()
    
    @classmethod
    def _create_test_tables(cls):
        """Create test tables"""
        with connection.cursor() as cursor:
            # Check if test user exists
            cursor.execute("SELECT ID FROM users_master WHERE EMP_ID = 'TEST001' LIMIT 1")
            row = cursor.fetchone()
            if not row:
                cursor.execute("""
                    INSERT INTO users_master (EMP_ID, EMP_NAME, EMAIL, ROLE, PASSWORD, IS_FIRST_LOGIN, CREATED_AT, UPDATED_AT)
                    VALUES ('TEST001', 'Test User', 'test@example.com', 'TESTER', 'test', 0, NOW(), NOW())
                """)
                cls.test_user_id = cursor.lastrowid
            else:
                cls.test_user_id = row[0]
            
            # Create admin user
            cursor.execute("SELECT ID FROM users_master WHERE EMP_ID = 'ADMIN001' LIMIT 1")
            row = cursor.fetchone()
            if not row:
                cursor.execute("""
                    INSERT INTO users_master (EMP_ID, EMP_NAME, EMAIL, ROLE, PASSWORD, IS_FIRST_LOGIN, CREATED_AT, UPDATED_AT)
                    VALUES ('ADMIN001', 'Admin User', 'admin@example.com', 'ADMIN', 'admin', 0, NOW(), NOW())
                """)
                cls.admin_user_id = cursor.lastrowid
            else:
                cls.admin_user_id = row[0]
    
    def setUp(self):
        """Set up test data"""
        self.test_user_id = self.__class__.test_user_id
        self.admin_user_id = self.__class__.admin_user_id
    
    def tearDown(self):
        """Clean up test data"""
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM attendance_leave_audit WHERE leave_id IN (SELECT id FROM attendance_leave_v2 WHERE notes LIKE 'TEST_%')")
            cursor.execute("DELETE FROM attendance_leave_v2 WHERE notes LIKE 'TEST_%'")
    
    # ============================================
    # CREATE LEAVE TESTS
    # ============================================
    
    def test_create_leave_creates_row_and_audit(self):
        """Test that creating a leave creates both the leave record and audit entry"""
        leave_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        leave_id, editable_until = models.create_leave(
            user_id=self.test_user_id,
            leave_date=leave_date,
            leave_type='PLANNED',
            notes='TEST_create_leave'
        )
        
        # Verify leave was created
        self.assertIsNotNone(leave_id)
        self.assertIsNotNone(editable_until)
        
        # Verify leave record
        leave = models.get_leave_by_id(leave_id)
        self.assertIsNotNone(leave)
        self.assertEqual(leave['status'], 'PENDING')
        self.assertEqual(leave['leave_type'], 'PLANNED')
        
        # Verify audit record
        audit = models.get_audit_trail(leave_id)
        self.assertEqual(len(audit), 1)
        self.assertEqual(audit[0]['action'], 'CREATED')
        self.assertEqual(audit[0]['actor_id'], self.test_user_id)
        self.assertEqual(audit[0]['actor_role'], 'USER')
    
    def test_create_leave_sets_editable_until(self):
        """Test that editable_until is set to created_at + 10 minutes"""
        leave_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        leave_id, editable_until = models.create_leave(
            user_id=self.test_user_id,
            leave_date=leave_date,
            leave_type='CASUAL',
            notes='TEST_editable_until'
        )
        
        leave = models.get_leave_raw(leave_id)
        created_at = leave['created_at']
        expected_editable_until = created_at + timedelta(minutes=models.EDIT_WINDOW_MINUTES)
        
        # Allow 1 second tolerance
        actual_editable_until = leave['editable_until']
        diff = abs((actual_editable_until - expected_editable_until).total_seconds())
        self.assertLess(diff, 2)
    
    # ============================================
    # EDIT WINDOW TESTS
    # ============================================
    
    def test_check_edit_window_within_window(self):
        """Test that edit window check returns True within 10 minutes"""
        leave_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        leave_id, _ = models.create_leave(
            user_id=self.test_user_id,
            leave_date=leave_date,
            leave_type='PLANNED',
            notes='TEST_edit_window_within'
        )
        
        is_editable, message, seconds_remaining = models.check_edit_window(leave_id, self.test_user_id)
        
        self.assertTrue(is_editable)
        self.assertEqual(message, 'Editable')
        self.assertGreater(seconds_remaining, 0)
        self.assertLessEqual(seconds_remaining, models.EDIT_WINDOW_MINUTES * 60)
    
    def test_check_edit_window_wrong_user(self):
        """Test that edit window check fails for wrong user"""
        leave_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        leave_id, _ = models.create_leave(
            user_id=self.test_user_id,
            leave_date=leave_date,
            leave_type='PLANNED',
            notes='TEST_edit_window_wrong_user'
        )
        
        # Try to check with different user
        is_editable, message, _ = models.check_edit_window(leave_id, self.admin_user_id)
        
        self.assertFalse(is_editable)
        self.assertIn('not authorized', message.lower())
    
    def test_check_edit_window_non_pending_status(self):
        """Test that edit window check fails for non-PENDING status"""
        leave_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        leave_id, _ = models.create_leave(
            user_id=self.test_user_id,
            leave_date=leave_date,
            leave_type='PLANNED',
            notes='TEST_edit_window_approved'
        )
        
        # Approve the leave
        models.approve_leave_admin(leave_id, self.admin_user_id, 'Approved for test')
        
        # Try to check edit window
        is_editable, message, _ = models.check_edit_window(leave_id, self.test_user_id)
        
        self.assertFalse(is_editable)
        self.assertIn('APPROVED', message)
    
    @patch('adminpanel.leave_models.get_ist_now')
    def test_user_cannot_edit_after_10_minutes(self, mock_now):
        """Test that user cannot edit after 10 minutes (simulated time jump)"""
        # Create leave at "current" time
        real_now = datetime.now(IST)
        mock_now.return_value = real_now
        
        leave_date = (real_now + timedelta(days=1)).strftime('%Y-%m-%d')
        
        leave_id, editable_until = models.create_leave(
            user_id=self.test_user_id,
            leave_date=leave_date,
            leave_type='PLANNED',
            notes='TEST_edit_after_10_min'
        )
        
        # Simulate time jump to 11 minutes later
        mock_now.return_value = real_now + timedelta(minutes=11)
        
        # Try to edit
        success, message = models.update_leave_user(
            leave_id, self.test_user_id,
            leave_date=leave_date,
            leave_type='CASUAL',
            notes='TEST_edit_after_10_min_updated'
        )
        
        self.assertFalse(success)
        self.assertIn('expired', message.lower())
    
    # ============================================
    # UPDATE LEAVE TESTS
    # ============================================
    
    def test_update_leave_within_window(self):
        """Test that user can update leave within edit window"""
        leave_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        new_leave_date = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
        
        leave_id, _ = models.create_leave(
            user_id=self.test_user_id,
            leave_date=leave_date,
            leave_type='PLANNED',
            notes='TEST_update_within_window'
        )
        
        success, message = models.update_leave_user(
            leave_id, self.test_user_id,
            leave_date=new_leave_date,
            leave_type='CASUAL',
            notes='TEST_update_within_window_updated'
        )
        
        self.assertTrue(success)
        
        # Verify update
        leave = models.get_leave_by_id(leave_id)
        self.assertEqual(leave['leave_type'], 'CASUAL')
        
        # Verify audit
        audit = models.get_audit_trail(leave_id)
        self.assertEqual(len(audit), 2)  # CREATE + EDIT
        self.assertEqual(audit[0]['action'], 'EDITED')
    
    def test_update_leave_does_not_extend_window(self):
        """Test that editing does not extend the edit window"""
        leave_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        leave_id, original_editable_until = models.create_leave(
            user_id=self.test_user_id,
            leave_date=leave_date,
            leave_type='PLANNED',
            notes='TEST_no_extend_window'
        )
        
        # Wait a moment and update
        import time
        time.sleep(0.5)
        
        success, _ = models.update_leave_user(
            leave_id, self.test_user_id,
            leave_date=leave_date,
            leave_type='CASUAL',
            notes='TEST_no_extend_window_updated'
        )
        
        self.assertTrue(success)
        
        # Verify editable_until hasn't changed
        leave = models.get_leave_raw(leave_id)
        # The editable_until should be the same (within 1 second tolerance)
        diff = abs((leave['editable_until'] - original_editable_until.replace(tzinfo=None)).total_seconds())
        self.assertLess(diff, 2)
    
    # ============================================
    # ADMIN APPROVE/REJECT TESTS
    # ============================================
    
    def test_admin_can_approve(self):
        """Test that admin can approve a pending leave"""
        leave_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        leave_id, _ = models.create_leave(
            user_id=self.test_user_id,
            leave_date=leave_date,
            leave_type='PLANNED',
            notes='TEST_admin_approve'
        )
        
        success, message, leave_data = models.approve_leave_admin(
            leave_id, self.admin_user_id, 'Approved by admin'
        )
        
        self.assertTrue(success)
        self.assertIsNotNone(leave_data)
        self.assertEqual(leave_data['status'], 'APPROVED')
        
        # Verify audit
        audit = models.get_audit_trail(leave_id)
        approve_audit = [a for a in audit if a['action'] == 'APPROVED']
        self.assertEqual(len(approve_audit), 1)
        self.assertEqual(approve_audit[0]['actor_role'], 'ADMIN')
    
    def test_admin_can_reject_with_reason(self):
        """Test that admin can reject with reason"""
        leave_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        leave_id, _ = models.create_leave(
            user_id=self.test_user_id,
            leave_date=leave_date,
            leave_type='PLANNED',
            notes='TEST_admin_reject'
        )
        
        success, message, leave_data = models.reject_leave_admin(
            leave_id, self.admin_user_id,
            reason='Project deadline',
            approval_notes='Cannot approve due to project deadline'
        )
        
        self.assertTrue(success)
        self.assertEqual(leave_data['status'], 'REJECTED')
        
        # Verify audit has reason
        audit = models.get_audit_trail(leave_id)
        reject_audit = [a for a in audit if a['action'] == 'REJECTED']
        self.assertEqual(len(reject_audit), 1)
        self.assertEqual(reject_audit[0]['reason'], 'Project deadline')
    
    def test_cannot_approve_already_approved(self):
        """Test that cannot approve an already approved leave"""
        leave_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        leave_id, _ = models.create_leave(
            user_id=self.test_user_id,
            leave_date=leave_date,
            leave_type='PLANNED',
            notes='TEST_double_approve'
        )
        
        # First approval
        models.approve_leave_admin(leave_id, self.admin_user_id, 'First approval')
        
        # Try second approval
        success, message, _ = models.approve_leave_admin(leave_id, self.admin_user_id, 'Second approval')
        
        self.assertFalse(success)
        self.assertIn('APPROVED', message)
    
    # ============================================
    # CANCEL LEAVE TESTS
    # ============================================
    
    def test_user_can_cancel_pending_leave(self):
        """Test that user can cancel their pending leave"""
        leave_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        leave_id, _ = models.create_leave(
            user_id=self.test_user_id,
            leave_date=leave_date,
            leave_type='PLANNED',
            notes='TEST_user_cancel'
        )
        
        success, message = models.cancel_leave_user(
            leave_id, self.test_user_id, 'Changed plans'
        )
        
        self.assertTrue(success)
        
        # Verify status
        leave = models.get_leave_by_id(leave_id)
        self.assertEqual(leave['status'], 'CANCELLED')
    
    def test_user_cannot_cancel_approved_leave(self):
        """Test that user cannot cancel an approved leave"""
        leave_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        leave_id, _ = models.create_leave(
            user_id=self.test_user_id,
            leave_date=leave_date,
            leave_type='PLANNED',
            notes='TEST_cancel_approved'
        )
        
        # Approve first
        models.approve_leave_admin(leave_id, self.admin_user_id, 'Approved')
        
        # Try to cancel
        success, message = models.cancel_leave_user(leave_id, self.test_user_id, 'Want to cancel')
        
        self.assertFalse(success)
        self.assertIn('APPROVED', message)
    
    # ============================================
    # ADMIN EDIT TESTS
    # ============================================
    
    def test_admin_can_edit_anytime(self):
        """Test that admin can edit leave anytime regardless of edit window"""
        leave_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        new_leave_date = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
        
        leave_id, _ = models.create_leave(
            user_id=self.test_user_id,
            leave_date=leave_date,
            leave_type='PLANNED',
            notes='TEST_admin_edit'
        )
        
        # Admin edit
        success, message = models.update_leave_admin(
            leave_id, self.admin_user_id,
            leave_date=new_leave_date,
            leave_type='EMERGENCY',
            notes='TEST_admin_edit_updated'
        )
        
        self.assertTrue(success)
        
        # Verify
        leave = models.get_leave_by_id(leave_id)
        self.assertEqual(leave['leave_type'], 'EMERGENCY')
        
        # Verify audit shows admin edit
        audit = models.get_audit_trail(leave_id)
        edit_audit = [a for a in audit if a['action'] == 'EDITED']
        self.assertEqual(len(edit_audit), 1)
        self.assertEqual(edit_audit[0]['actor_role'], 'ADMIN')


class LeaveViewTestCase(TestCase):
    """Test cases for leave views (API endpoints)"""
    
    def setUp(self):
        """Set up test client and user"""
        self.client = Client()
        # Note: These tests require proper authentication setup
        # For now, they serve as documentation of expected behavior
    
    def test_create_leave_endpoint_requires_auth(self):
        """Test that create endpoint requires authentication"""
        response = self.client.post('/user/leave/v2/create/', 
            data=json.dumps({'leave_date': '2025-12-01', 'leave_type': 'PLANNED'}),
            content_type='application/json'
        )
        # Should redirect to login or return 403
        self.assertIn(response.status_code, [302, 403])
    
    def test_admin_approve_endpoint_requires_admin(self):
        """Test that approve endpoint requires admin role"""
        response = self.client.post('/admin/leave/v2/1/approve/',
            data=json.dumps({'approval_notes': 'Test'}),
            content_type='application/json'
        )
        # Should redirect to login or return 403
        self.assertIn(response.status_code, [302, 403])


# ============================================
# RUN TESTS
# ============================================
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
