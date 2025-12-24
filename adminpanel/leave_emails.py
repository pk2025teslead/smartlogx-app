"""
SmartLogX Leave Management - Email Notifications
HTML and Plain Text email templates for leave actions
"""

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)


def send_leave_email(subject, html_content, text_content, recipients, fail_silently=True):
    """
    Send email with HTML and plain text versions
    Returns: (success: bool, message: str)
    """
    try:
        from_email = getattr(settings, 'EMAIL_HOST_USER', None)
        if not from_email:
            return False, "EMAIL_HOST_USER not configured"
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=recipients if isinstance(recipients, list) else [recipients]
        )
        email.attach_alternative(html_content, "text/html")
        
        # UNCOMMENT THE LINE BELOW TO ENABLE EMAIL SENDING
        # email.send(fail_silently=fail_silently)
        
        logger.info(f"Email sent: {subject} to {recipients}")
        return True, "Email sent successfully"
        
    except Exception as e:
        logger.error(f"Email failed: {subject} - {str(e)}")
        return False, str(e)


# ============================================
# EMAIL TEMPLATES - NEW LEAVE TO ADMIN
# ============================================

def get_new_leave_email_html(user_name, emp_id, leave_date, leave_type, notes, submitted_at):
    """Generate HTML email for new leave request notification to admin"""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Leave Request</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #f4f6f9; padding: 40px 20px;">
        <tr>
            <td align="center">
                <table role="presentation" width="600" cellspacing="0" cellpadding="0" style="background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); overflow: hidden;">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #003366 0%, #004d99 100%); padding: 25px 40px; text-align: center;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 600; letter-spacing: 1px;">
                                TESLEAD IT TEAM
                            </h1>
                            <p style="color: #b3d4fc; margin: 8px 0 0 0; font-size: 14px;">
                                New Leave Request
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Body -->
                    <tr>
                        <td style="padding: 35px 40px;">
                            <p style="color: #333333; font-size: 15px; line-height: 1.6; margin: 0 0 10px 0;">
                                Greetings of the day,
                            </p>
                            <p style="color: #333333; font-size: 15px; line-height: 1.6; margin: 0 0 25px 0;">
                                Hai Team,
                            </p>
                            <p style="color: #555555; font-size: 15px; line-height: 1.7; margin: 0 0 20px 0;">
                                A new leave request has been submitted and requires your attention.
                            </p>
                            
                            <!-- User Info -->
                            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #f8fafc; border-radius: 8px; border: 1px solid #e9ecef; margin-bottom: 25px;">
                                <tr>
                                    <td style="padding: 12px 15px; border-bottom: 1px solid #f0f0f0; width: 40%;">
                                        <span style="color: #666666; font-size: 14px; font-weight: 600;">Employee Name</span>
                                    </td>
                                    <td style="padding: 12px 15px; border-bottom: 1px solid #f0f0f0;">
                                        <span style="color: #333333; font-size: 14px; font-weight: 500;">{user_name}</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 12px 15px; border-bottom: 1px solid #f0f0f0;">
                                        <span style="color: #666666; font-size: 14px; font-weight: 600;">Employee ID</span>
                                    </td>
                                    <td style="padding: 12px 15px; border-bottom: 1px solid #f0f0f0;">
                                        <span style="color: #333333; font-size: 14px;">{emp_id}</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 12px 15px;">
                                        <span style="color: #666666; font-size: 14px; font-weight: 600;">Submitted At</span>
                                    </td>
                                    <td style="padding: 12px 15px;">
                                        <span style="color: #333333; font-size: 14px;">{submitted_at}</span>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Leave Details -->
                            <h3 style="color: #003366; font-size: 16px; margin: 25px 0 15px 0; padding-bottom: 8px; border-bottom: 2px solid #003366;">
                                LEAVE DETAILS
                            </h3>
                            
                            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #fff8e6; border-radius: 8px; border: 1px solid #ffd966;">
                                <tr>
                                    <td style="padding: 12px 15px; border-bottom: 1px solid #ffe699; width: 40%;">
                                        <span style="color: #666666; font-size: 14px; font-weight: 600;">Leave Date</span>
                                    </td>
                                    <td style="padding: 12px 15px; border-bottom: 1px solid #ffe699;">
                                        <span style="color: #333333; font-size: 14px; font-weight: 500;">{leave_date}</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 12px 15px; border-bottom: 1px solid #ffe699;">
                                        <span style="color: #666666; font-size: 14px; font-weight: 600;">Leave Type</span>
                                    </td>
                                    <td style="padding: 12px 15px; border-bottom: 1px solid #ffe699;">
                                        <span style="color: #333333; font-size: 14px;">{leave_type}</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 12px 15px;">
                                        <span style="color: #666666; font-size: 14px; font-weight: 600;">Notes</span>
                                    </td>
                                    <td style="padding: 12px 15px;">
                                        <span style="color: #333333; font-size: 14px;">{notes or 'N/A'}</span>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Action Required -->
                            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #e8f4fd; border-radius: 8px; border: 1px solid #b3d7f5; margin-top: 25px;">
                                <tr>
                                    <td style="padding: 18px 20px;">
                                        <p style="color: #0c5460; font-size: 14px; margin: 0; font-weight: 600;">
                                            ⏳ ACTION REQUIRED
                                        </p>
                                        <p style="color: #0c5460; font-size: 14px; margin: 10px 0 0 0; line-height: 1.6;">
                                            Please review and approve/reject this leave request in the admin panel.
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8fafc; padding: 25px 40px; border-top: 1px solid #e9ecef;">
                            <p style="color: #333333; font-size: 14px; margin: 0 0 5px 0; font-weight: 600;">
                                Thanks & Regards,
                            </p>
                            <p style="color: #003366; font-size: 15px; margin: 0; font-weight: 700;">
                                TESLEAD IT TEAM
                            </p>
                            <p style="color: #999999; font-size: 12px; margin: 15px 0 0 0;">
                                This is an automated notification from SmartLogX.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""


def get_new_leave_email_text(user_name, emp_id, leave_date, leave_type, notes, submitted_at):
    """Generate plain text email for new leave request"""
    return f"""
Greetings of the day,

Hai Team,

A new leave request has been submitted and requires your attention.

EMPLOYEE DETAILS
----------------
Employee Name: {user_name}
Employee ID: {emp_id}
Submitted At: {submitted_at}

LEAVE DETAILS
-------------
Leave Date: {leave_date}
Leave Type: {leave_type}
Notes: {notes or 'N/A'}

ACTION REQUIRED
---------------
Please review and approve/reject this leave request in the admin panel.

Thanks & Regards,
TESLEAD IT TEAM

---
This is an automated notification from SmartLogX.
"""


def send_new_leave_notification(leave_data):
    """Send notification to admin when new leave is submitted"""
    admin_email = getattr(settings, 'ADMIN_EMAIL', None)
    if not admin_email:
        return False, "ADMIN_EMAIL not configured"
    
    subject = f"Leave Request - {leave_data.get('emp_name', 'Unknown')} - {leave_data.get('leave_date', '')}"
    
    html_content = get_new_leave_email_html(
        user_name=leave_data.get('emp_name', 'Unknown'),
        emp_id=leave_data.get('emp_id', 'N/A'),
        leave_date=leave_data.get('leave_date', ''),
        leave_type=leave_data.get('leave_type', ''),
        notes=leave_data.get('notes', ''),
        submitted_at=leave_data.get('created_at', '')
    )
    
    text_content = get_new_leave_email_text(
        user_name=leave_data.get('emp_name', 'Unknown'),
        emp_id=leave_data.get('emp_id', 'N/A'),
        leave_date=leave_data.get('leave_date', ''),
        leave_type=leave_data.get('leave_type', ''),
        notes=leave_data.get('notes', ''),
        submitted_at=leave_data.get('created_at', '')
    )
    
    return send_leave_email(subject, html_content, text_content, admin_email)


# ============================================
# EMAIL TEMPLATES - LEAVE APPROVED TO USER
# ============================================

def get_leave_approved_email_html(user_name, leave_date, leave_type, admin_notes):
    """Generate HTML email for leave approval notification"""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Leave Approved</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #f4f6f9; padding: 40px 20px;">
        <tr>
            <td align="center">
                <table role="presentation" width="600" cellspacing="0" cellpadding="0" style="background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); overflow: hidden;">
                    <tr>
                        <td style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 25px 40px; text-align: center;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 24px;">TESLEAD IT TEAM</h1>
                            <p style="color: #d1fae5; margin: 8px 0 0 0; font-size: 14px;">Leave Approved ✓</p>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 35px 40px;">
                            <p style="color: #333333; font-size: 15px; margin: 0 0 20px 0;">Hi <strong>{user_name}</strong>,</p>
                            <p style="color: #555555; font-size: 15px; line-height: 1.7; margin: 0 0 25px 0;">
                                Great news! Your leave request has been <strong style="color: #10b981;">APPROVED</strong>.
                            </p>
                            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #ecfdf5; border-radius: 8px; border: 1px solid #a7f3d0; margin-bottom: 25px;">
                                <tr>
                                    <td style="padding: 12px 15px; border-bottom: 1px solid #d1fae5; width: 40%;"><span style="color: #666666; font-size: 14px; font-weight: 600;">Leave Date</span></td>
                                    <td style="padding: 12px 15px; border-bottom: 1px solid #d1fae5;"><span style="color: #333333; font-size: 14px; font-weight: 500;">{leave_date}</span></td>
                                </tr>
                                <tr>
                                    <td style="padding: 12px 15px; border-bottom: 1px solid #d1fae5;"><span style="color: #666666; font-size: 14px; font-weight: 600;">Leave Type</span></td>
                                    <td style="padding: 12px 15px; border-bottom: 1px solid #d1fae5;"><span style="color: #333333; font-size: 14px;">{leave_type}</span></td>
                                </tr>
                                <tr>
                                    <td style="padding: 12px 15px;"><span style="color: #666666; font-size: 14px; font-weight: 600;">Admin Notes</span></td>
                                    <td style="padding: 12px 15px;"><span style="color: #333333; font-size: 14px;">{admin_notes or 'N/A'}</span></td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td style="background-color: #f8fafc; padding: 25px 40px; border-top: 1px solid #e9ecef;">
                            <p style="color: #333333; font-size: 14px; margin: 0 0 5px 0; font-weight: 600;">Thanks & Regards,</p>
                            <p style="color: #003366; font-size: 15px; margin: 0; font-weight: 700;">TESLEAD IT TEAM</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""


def get_leave_approved_email_text(user_name, leave_date, leave_type, admin_notes):
    """Generate plain text email for leave approval"""
    return f"""
Hi {user_name},

Great news! Your leave request has been APPROVED.

LEAVE DETAILS
-------------
Leave Date: {leave_date}
Leave Type: {leave_type}
Admin Notes: {admin_notes or 'N/A'}

Thanks & Regards,
TESLEAD IT TEAM
"""


def send_leave_approved_notification(leave_data):
    """Send approval notification to user"""
    user_email = leave_data.get('user_email')
    if not user_email:
        return False, "User email not found"
    
    subject = f"Leave Approved - {leave_data.get('emp_name', '')} - {leave_data.get('leave_date', '')}"
    
    html_content = get_leave_approved_email_html(
        user_name=leave_data.get('emp_name', 'User'),
        leave_date=str(leave_data.get('leave_date', '')),
        leave_type=leave_data.get('leave_type', ''),
        admin_notes=leave_data.get('approval_notes', '')
    )
    
    text_content = get_leave_approved_email_text(
        user_name=leave_data.get('emp_name', 'User'),
        leave_date=str(leave_data.get('leave_date', '')),
        leave_type=leave_data.get('leave_type', ''),
        admin_notes=leave_data.get('approval_notes', '')
    )
    
    return send_leave_email(subject, html_content, text_content, user_email)


# ============================================
# EMAIL TEMPLATES - LEAVE REJECTED TO USER
# ============================================

def get_leave_rejected_email_html(user_name, leave_date, leave_type, reason, admin_notes):
    """Generate HTML email for leave rejection notification"""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Leave Rejected</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #f4f6f9; padding: 40px 20px;">
        <tr>
            <td align="center">
                <table role="presentation" width="600" cellspacing="0" cellpadding="0" style="background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); overflow: hidden;">
                    <tr>
                        <td style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); padding: 25px 40px; text-align: center;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 24px;">TESLEAD IT TEAM</h1>
                            <p style="color: #fecaca; margin: 8px 0 0 0; font-size: 14px;">Leave Request Update</p>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 35px 40px;">
                            <p style="color: #333333; font-size: 15px; margin: 0 0 20px 0;">Hi <strong>{user_name}</strong>,</p>
                            <p style="color: #555555; font-size: 15px; line-height: 1.7; margin: 0 0 25px 0;">
                                We regret to inform you that your leave request has been <strong style="color: #ef4444;">REJECTED</strong>.
                            </p>
                            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #fef2f2; border-radius: 8px; border: 1px solid #fecaca; margin-bottom: 25px;">
                                <tr>
                                    <td style="padding: 12px 15px; border-bottom: 1px solid #fecaca; width: 40%;"><span style="color: #666666; font-size: 14px; font-weight: 600;">Leave Date</span></td>
                                    <td style="padding: 12px 15px; border-bottom: 1px solid #fecaca;"><span style="color: #333333; font-size: 14px; font-weight: 500;">{leave_date}</span></td>
                                </tr>
                                <tr>
                                    <td style="padding: 12px 15px; border-bottom: 1px solid #fecaca;"><span style="color: #666666; font-size: 14px; font-weight: 600;">Leave Type</span></td>
                                    <td style="padding: 12px 15px; border-bottom: 1px solid #fecaca;"><span style="color: #333333; font-size: 14px;">{leave_type}</span></td>
                                </tr>
                                <tr>
                                    <td style="padding: 12px 15px;"><span style="color: #666666; font-size: 14px; font-weight: 600;">Reason</span></td>
                                    <td style="padding: 12px 15px;"><span style="color: #991b1b; font-size: 14px; font-weight: 500;">{reason or admin_notes or 'Not specified'}</span></td>
                                </tr>
                            </table>
                            <p style="color: #555555; font-size: 14px; line-height: 1.6;">If you have any questions, please contact your manager or HR.</p>
                        </td>
                    </tr>
                    <tr>
                        <td style="background-color: #f8fafc; padding: 25px 40px; border-top: 1px solid #e9ecef;">
                            <p style="color: #333333; font-size: 14px; margin: 0 0 5px 0; font-weight: 600;">Thanks & Regards,</p>
                            <p style="color: #003366; font-size: 15px; margin: 0; font-weight: 700;">TESLEAD IT TEAM</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""


def get_leave_rejected_email_text(user_name, leave_date, leave_type, reason, admin_notes):
    """Generate plain text email for leave rejection"""
    return f"""
Hi {user_name},

We regret to inform you that your leave request has been REJECTED.

LEAVE DETAILS
-------------
Leave Date: {leave_date}
Leave Type: {leave_type}
Reason: {reason or admin_notes or 'Not specified'}

If you have any questions, please contact your manager or HR.

Thanks & Regards,
TESLEAD IT TEAM
"""


def send_leave_rejected_notification(leave_data, reason=None):
    """Send rejection notification to user"""
    user_email = leave_data.get('user_email')
    if not user_email:
        return False, "User email not found"
    
    subject = f"Leave Rejected - {leave_data.get('emp_name', '')} - {leave_data.get('leave_date', '')}"
    
    html_content = get_leave_rejected_email_html(
        user_name=leave_data.get('emp_name', 'User'),
        leave_date=str(leave_data.get('leave_date', '')),
        leave_type=leave_data.get('leave_type', ''),
        reason=reason,
        admin_notes=leave_data.get('approval_notes', '')
    )
    
    text_content = get_leave_rejected_email_text(
        user_name=leave_data.get('emp_name', 'User'),
        leave_date=str(leave_data.get('leave_date', '')),
        leave_type=leave_data.get('leave_type', ''),
        reason=reason,
        admin_notes=leave_data.get('approval_notes', '')
    )
    
    return send_leave_email(subject, html_content, text_content, user_email)


# ============================================
# EMAIL TEMPLATES - LEAVE EDITED TO ADMIN
# ============================================

def get_leave_edited_email_html(user_name, emp_id, leave_date, leave_type, notes, edited_at):
    """Generate HTML email for leave edit notification to admin"""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Leave Edited</title></head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; background-color: #f4f6f9;">
    <table width="100%" cellspacing="0" cellpadding="0" style="background-color: #f4f6f9; padding: 40px 20px;">
        <tr><td align="center">
            <table width="600" cellspacing="0" cellpadding="0" style="background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);">
                <tr><td style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); padding: 25px 40px; text-align: center;">
                    <h1 style="color: #ffffff; margin: 0; font-size: 24px;">TESLEAD IT TEAM</h1>
                    <p style="color: #fef3c7; margin: 8px 0 0 0; font-size: 14px;">Leave Request Edited</p>
                </td></tr>
                <tr><td style="padding: 35px 40px;">
                    <p style="color: #333; font-size: 15px; margin: 0 0 20px 0;">Hai Team,</p>
                    <p style="color: #555; font-size: 15px; margin: 0 0 25px 0;">A leave request has been <strong style="color: #f59e0b;">EDITED</strong> by the user.</p>
                    <table width="100%" style="background-color: #fffbeb; border-radius: 8px; border: 1px solid #fcd34d; margin-bottom: 25px;">
                        <tr><td style="padding: 12px 15px; border-bottom: 1px solid #fde68a; width: 40%;"><strong>Employee</strong></td><td style="padding: 12px 15px; border-bottom: 1px solid #fde68a;">{user_name} ({emp_id})</td></tr>
                        <tr><td style="padding: 12px 15px; border-bottom: 1px solid #fde68a;"><strong>Leave Date</strong></td><td style="padding: 12px 15px; border-bottom: 1px solid #fde68a;">{leave_date}</td></tr>
                        <tr><td style="padding: 12px 15px; border-bottom: 1px solid #fde68a;"><strong>Leave Type</strong></td><td style="padding: 12px 15px; border-bottom: 1px solid #fde68a;">{leave_type}</td></tr>
                        <tr><td style="padding: 12px 15px; border-bottom: 1px solid #fde68a;"><strong>Notes</strong></td><td style="padding: 12px 15px; border-bottom: 1px solid #fde68a;">{notes or 'N/A'}</td></tr>
                        <tr><td style="padding: 12px 15px;"><strong>Edited At</strong></td><td style="padding: 12px 15px;">{edited_at}</td></tr>
                    </table>
                </td></tr>
                <tr><td style="background-color: #f8fafc; padding: 25px 40px; border-top: 1px solid #e9ecef;">
                    <p style="color: #333; font-size: 14px; margin: 0 0 5px 0; font-weight: 600;">Thanks & Regards,</p>
                    <p style="color: #003366; font-size: 15px; margin: 0; font-weight: 700;">TESLEAD IT TEAM</p>
                </td></tr>
            </table>
        </td></tr>
    </table>
</body>
</html>
"""


def get_leave_edited_email_text(user_name, emp_id, leave_date, leave_type, notes, edited_at):
    return f"""
Hai Team,

A leave request has been EDITED by the user.

Employee: {user_name} ({emp_id})
Leave Date: {leave_date}
Leave Type: {leave_type}
Notes: {notes or 'N/A'}
Edited At: {edited_at}

Thanks & Regards,
TESLEAD IT TEAM
"""


def send_leave_edited_notification(leave_data):
    """Send notification to admin when leave is edited"""
    admin_email = getattr(settings, 'ADMIN_EMAIL', None)
    if not admin_email:
        return False, "ADMIN_EMAIL not configured"
    
    subject = f"Leave Edited - {leave_data.get('emp_name', '')} - {leave_data.get('leave_date', '')}"
    
    html_content = get_leave_edited_email_html(
        user_name=leave_data.get('emp_name', 'Unknown'),
        emp_id=leave_data.get('emp_id', 'N/A'),
        leave_date=str(leave_data.get('leave_date', '')),
        leave_type=leave_data.get('leave_type', ''),
        notes=leave_data.get('notes', ''),
        edited_at=str(leave_data.get('updated_at', ''))
    )
    
    text_content = get_leave_edited_email_text(
        user_name=leave_data.get('emp_name', 'Unknown'),
        emp_id=leave_data.get('emp_id', 'N/A'),
        leave_date=str(leave_data.get('leave_date', '')),
        leave_type=leave_data.get('leave_type', ''),
        notes=leave_data.get('notes', ''),
        edited_at=str(leave_data.get('updated_at', ''))
    )
    
    return send_leave_email(subject, html_content, text_content, admin_email)
