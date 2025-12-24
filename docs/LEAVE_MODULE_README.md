# SmartLogX Leave Management Module

## Overview

A production-ready Leave Management module for Django + MySQL using **RAW SQL only**. Features include:

- 10-minute edit window for user submissions
- Complete audit trail for all actions
- Email notifications for create/edit/approve/reject
- Server-side enforcement of all business rules
- Timezone: Asia/Kolkata (IST)

## Features

### User Features
- Submit leave requests (PLANNED, CASUAL, EMERGENCY, SICK)
- Edit requests within 10-minute window after submission
- Cancel pending requests
- View leave history with status

### Admin Features
- View all leave requests with filters
- Approve/Reject with notes
- Edit any leave request (no time restriction)
- View complete audit trail
- Soft delete (cancel) requests

### Edit Window Logic
- Users can edit their leave request for **10 minutes** after submission
- Timer displayed in UI with countdown
- Server-side enforcement (cannot bypass via API)
- Edit window does NOT reset on edit
- After window expires, only admin can modify

## Installation

### 1. Database Setup

Run the SQL script to create required tables:

```bash
mysql -u root -p smartlogx_db < smartlogx_leave_management.sql
```

Or execute in MySQL:

```sql
SOURCE /path/to/smartlogx_leave_management.sql;
```

### 2. Environment Variables

Add to your `.env` or `settings.py`:

```python
# Email Configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'

# Admin email for notifications
ADMIN_EMAIL = 'admin@yourcompany.com'
```

### 3. Enable Email Sending

In `adminpanel/leave_emails.py`, uncomment line 28:

```python
# Change this:
# email.send(fail_silently=fail_silently)

# To this:
email.send(fail_silently=fail_silently)
```

## URL Endpoints

### User Endpoints (prefix: `/user/leave/v2/`)

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | Leave list page |
| GET | `/<id>/` | Get leave detail (JSON) |
| POST | `/create/` | Create new leave |
| POST | `/<id>/edit/` | Edit leave (within window) |
| POST | `/<id>/cancel/` | Cancel leave |
| GET | `/<id>/check-edit/` | Check edit window status |

### Admin Endpoints (prefix: `/admin/leave/v2/`)

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | Leave list page |
| GET | `/list/` | Get leaves as JSON |
| GET | `/<id>/` | Get leave detail with audit |
| POST | `/<id>/update/` | Update leave |
| POST | `/<id>/delete/` | Soft delete leave |
| POST | `/<id>/approve/` | Approve leave |
| POST | `/<id>/reject/` | Reject leave |
| GET | `/<id>/audit/` | Get audit trail |

## Database Schema

### attendance_leave_v2

| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| user_id | INT | FK to users_master |
| leave_date | DATE | Date of leave |
| leave_type | VARCHAR(50) | PLANNED/CASUAL/EMERGENCY/SICK |
| notes | TEXT | User notes |
| status | VARCHAR(20) | PENDING/APPROVED/REJECTED/CANCELLED |
| is_editable | BOOLEAN | Edit window flag |
| created_at | DATETIME | Creation timestamp |
| editable_until | DATETIME | Edit window expiry |
| updated_at | DATETIME | Last update |
| created_by | INT | Creator user ID |
| approved_by | INT | Approver admin ID |
| approved_at | DATETIME | Approval timestamp |
| approval_notes | TEXT | Admin notes |

### attendance_leave_audit

| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| leave_id | INT | FK to attendance_leave_v2 |
| action | VARCHAR(50) | CREATED/EDITED/APPROVED/REJECTED/CANCELLED/DELETED |
| actor_id | INT | User who performed action |
| actor_role | VARCHAR(50) | USER/ADMIN |
| actor_name | VARCHAR(255) | Cached actor name |
| old_data | JSON | Previous values |
| new_data | JSON | New values |
| reason | TEXT | Action reason |
| ip_address | VARCHAR(45) | Client IP |
| created_at | DATETIME | Action timestamp |

## Configuration

### Adjusting Edit Window Duration

In `adminpanel/leave_models.py`, change:

```python
EDIT_WINDOW_MINUTES = 10  # Change to desired minutes
```

### Email Templates

Located in `adminpanel/leave_emails.py`:

- `get_new_leave_email_html()` - New leave to admin
- `get_leave_approved_email_html()` - Approval to user
- `get_leave_rejected_email_html()` - Rejection to user
- `get_leave_edited_email_html()` - Edit notification to admin

## Running Tests

```bash
# Run all leave module tests
python manage.py test tests.test_leave_module

# Run with pytest
pytest tests/test_leave_module.py -v

# Run specific test
pytest tests/test_leave_module.py::LeaveModelTestCase::test_create_leave_creates_row_and_audit -v
```

## API Response Format

### Success Response
```json
{
    "success": true,
    "message": "Leave request submitted successfully",
    "id": 123,
    "editable_until": "29-Nov-2025 14:30 IST",
    "seconds_remaining": 600
}
```

### Error Response
```json
{
    "success": false,
    "error": "Edit window expired at 29-Nov-2025 14:20 IST"
}
```

### Validation Errors
```json
{
    "success": false,
    "errors": [
        "Leave date is required",
        "Leave type is required"
    ]
}
```

## Security Considerations

1. **SQL Injection**: All queries use parameterized statements
2. **CSRF Protection**: All POST endpoints require CSRF token
3. **Authentication**: All endpoints require login
4. **Authorization**: User endpoints check ownership, admin endpoints check is_staff
5. **Race Conditions**: Uses `SELECT ... FOR UPDATE` for concurrent access

## Troubleshooting

### Edit window not working
- Ensure server timezone is set to Asia/Kolkata
- Check `editable_until` column is being set correctly
- Verify client-side timer is synced with server

### Emails not sending
- Check EMAIL_* settings in settings.py
- Uncomment `email.send()` line in leave_emails.py
- Check email logs for errors

### Audit trail missing
- Ensure `attendance_leave_audit` table exists
- Check for transaction rollbacks
- Verify `insert_audit()` is being called

## File Structure

```
adminpanel/
├── leave_models.py      # Raw SQL models & business logic
├── leave_views.py       # Admin views
├── leave_emails.py      # Email templates & sending

userpanel/
├── leave_views.py       # User views

templates/
├── adminpanel/
│   └── leave_list_admin_v2.html
├── userpanel/
│   └── leave_list_user_v2.html

tests/
└── test_leave_module.py

docs/
└── LEAVE_MODULE_README.md

smartlogx_leave_management.sql  # Database schema
```

## Version History

- **v2.0** - Enhanced with 10-minute edit window and audit trail
- **v1.0** - Basic leave management (legacy)
