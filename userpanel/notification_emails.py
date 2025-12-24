"""
User Notification Email System for TESLEAD IT Team
Sends email notifications to Admin when users submit requests.

Supported request types:
- Leave Request
- Work From Home (WFH) Request
- Comp-Off Request
- Log Submission
"""

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


# ============================================
# EMAIL TEMPLATE GENERATORS
# ============================================

def get_base_html_template(title, content_html):
    """
    Base HTML email template with TESLEAD branding.
    Clean, corporate design compatible with Gmail, Outlook, Mobile.
    """
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
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
                                {title}
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Body Content -->
                    <tr>
                        <td style="padding: 35px 40px;">
                            {content_html}
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


def get_info_row_html(label, value):
    """Generate a single info row for the email body"""
    return f"""
    <tr>
        <td style="padding: 10px 15px; border-bottom: 1px solid #f0f0f0; width: 40%;">
            <span style="color: #666666; font-size: 14px; font-weight: 600;">{label}</span>
        </td>
        <td style="padding: 10px 15px; border-bottom: 1px solid #f0f0f0;">
            <span style="color: #333333; font-size: 14px;">{value}</span>
        </td>
    </tr>
    """


# ============================================
# LEAVE REQUEST EMAIL
# ============================================

def get_leave_request_html(user_name, emp_id, leave_date, leave_type, notes):
    """Generate HTML content for leave request email"""
    content = f"""
    <p style="color: #333333; font-size: 15px; line-height: 1.6; margin: 0 0 10px 0;">
        Greetings of the day,
    </p>
    <p style="color: #333333; font-size: 15px; line-height: 1.6; margin: 0 0 25px 0;">
        Hai Team,
    </p>
    <p style="color: #555555; font-size: 15px; line-height: 1.7; margin: 0 0 20px 0;">
        Please find the information submitted by the user.
    </p>
    
    <!-- User Info Card -->
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #f8fafc; border-radius: 8px; border: 1px solid #e9ecef; margin-bottom: 25px;">
        {get_info_row_html("User Name", user_name)}
        {get_info_row_html("Employee ID", emp_id)}
        {get_info_row_html("Date", leave_date)}
    </table>
    
    <!-- Request Details -->
    <h3 style="color: #003366; font-size: 16px; margin: 25px 0 15px 0; padding-bottom: 8px; border-bottom: 2px solid #003366;">
        REQUEST DETAILS
    </h3>
    
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #fff8e6; border-radius: 8px; border: 1px solid #ffd966;">
        {get_info_row_html("Leave Type", leave_type)}
        {get_info_row_html("Notes", notes if notes else "N/A")}
    </table>
    """
    return content


def get_leave_request_plain_text(user_name, emp_id, leave_date, leave_type, notes):
    """Generate plain text content for leave request email"""
    return f"""
Greetings of the day,

Hai Team,

Please find the information submitted by the user.

User Name    : {user_name}
Employee ID  : {emp_id}
Date         : {leave_date}

REQUEST DETAILS:
----------------
Leave Type   : {leave_type}
Notes        : {notes if notes else "N/A"}

----------------------------------------

Thanks & Regards,
TESLEAD IT TEAM
"""


# ============================================
# WFH REQUEST EMAIL
# ============================================

def get_wfh_request_html(user_name, emp_id, wfh_date, reason, notes):
    """Generate HTML content for WFH request email"""
    content = f"""
    <p style="color: #333333; font-size: 15px; line-height: 1.6; margin: 0 0 10px 0;">
        Greetings of the day,
    </p>
    <p style="color: #333333; font-size: 15px; line-height: 1.6; margin: 0 0 25px 0;">
        Hai Team,
    </p>
    <p style="color: #555555; font-size: 15px; line-height: 1.7; margin: 0 0 20px 0;">
        Please find the information submitted by the user.
    </p>
    
    <!-- User Info Card -->
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #f8fafc; border-radius: 8px; border: 1px solid #e9ecef; margin-bottom: 25px;">
        {get_info_row_html("User Name", user_name)}
        {get_info_row_html("Employee ID", emp_id)}
        {get_info_row_html("Date", wfh_date)}
    </table>
    
    <!-- Request Details -->
    <h3 style="color: #003366; font-size: 16px; margin: 25px 0 15px 0; padding-bottom: 8px; border-bottom: 2px solid #003366;">
        REQUEST DETAILS
    </h3>
    
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #e8f4fd; border-radius: 8px; border: 1px solid #b3d7f5;">
        {get_info_row_html("Work From Reason", reason)}
        {get_info_row_html("Notes", notes if notes else "N/A")}
    </table>
    """
    return content


def get_wfh_request_plain_text(user_name, emp_id, wfh_date, reason, notes):
    """Generate plain text content for WFH request email"""
    return f"""
Greetings of the day,

Hai Team,

Please find the information submitted by the user.

User Name    : {user_name}
Employee ID  : {emp_id}
Date         : {wfh_date}

REQUEST DETAILS:
----------------
Work From Reason : {reason}
Notes            : {notes if notes else "N/A"}

----------------------------------------

Thanks & Regards,
TESLEAD IT TEAM
"""


# ============================================
# COMP-OFF REQUEST EMAIL
# ============================================

def get_compoff_request_html(user_name, emp_id, request_date, sunday_date, work_purpose, compoff_date, notes):
    """Generate HTML content for comp-off request email"""
    compoff_display = compoff_date if compoff_date else "No Comp-Off"
    
    content = f"""
    <p style="color: #333333; font-size: 15px; line-height: 1.6; margin: 0 0 10px 0;">
        Greetings of the day,
    </p>
    <p style="color: #333333; font-size: 15px; line-height: 1.6; margin: 0 0 25px 0;">
        Hai Team,
    </p>
    <p style="color: #555555; font-size: 15px; line-height: 1.7; margin: 0 0 20px 0;">
        Please find the information submitted by the user.
    </p>
    
    <!-- User Info Card -->
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #f8fafc; border-radius: 8px; border: 1px solid #e9ecef; margin-bottom: 25px;">
        {get_info_row_html("User Name", user_name)}
        {get_info_row_html("Employee ID", emp_id)}
        {get_info_row_html("Date", request_date)}
    </table>
    
    <!-- Request Details -->
    <h3 style="color: #003366; font-size: 16px; margin: 25px 0 15px 0; padding-bottom: 8px; border-bottom: 2px solid #003366;">
        REQUEST DETAILS
    </h3>
    
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #f0fff4; border-radius: 8px; border: 1px solid #9ae6b4;">
        {get_info_row_html("Sunday Worked On", sunday_date)}
        {get_info_row_html("Work Purpose", work_purpose)}
        {get_info_row_html("Comp-Off Date", compoff_display)}
        {get_info_row_html("Notes", notes if notes else "N/A")}
    </table>
    """
    return content


def get_compoff_request_plain_text(user_name, emp_id, request_date, sunday_date, work_purpose, compoff_date, notes):
    """Generate plain text content for comp-off request email"""
    compoff_display = compoff_date if compoff_date else "No Comp-Off"
    
    return f"""
Greetings of the day,

Hai Team,

Please find the information submitted by the user.

User Name    : {user_name}
Employee ID  : {emp_id}
Date         : {request_date}

REQUEST DETAILS:
----------------
Sunday Worked On : {sunday_date}
Work Purpose     : {work_purpose}
Comp-Off Date    : {compoff_display}
Notes            : {notes if notes else "N/A"}

----------------------------------------

Thanks & Regards,
TESLEAD IT TEAM
"""


# ============================================
# LOG SUBMISSION EMAIL
# ============================================

def get_log_submission_html(user_name, emp_id, log_date, project_title, log_heading, session, description):
    """Generate HTML content for log submission email"""
    # Truncate description if too long
    desc_display = description[:500] + "..." if len(description) > 500 else description
    
    content = f"""
    <p style="color: #333333; font-size: 15px; line-height: 1.6; margin: 0 0 10px 0;">
        Greetings of the day,
    </p>
    <p style="color: #333333; font-size: 15px; line-height: 1.6; margin: 0 0 25px 0;">
        Hai Team,
    </p>
    <p style="color: #555555; font-size: 15px; line-height: 1.7; margin: 0 0 20px 0;">
        Please find the information submitted by the user.
    </p>
    
    <!-- User Info Card -->
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #f8fafc; border-radius: 8px; border: 1px solid #e9ecef; margin-bottom: 25px;">
        {get_info_row_html("User Name", user_name)}
        {get_info_row_html("Employee ID", emp_id)}
        {get_info_row_html("Date", log_date)}
    </table>
    
    <!-- Request Details -->
    <h3 style="color: #003366; font-size: 16px; margin: 25px 0 15px 0; padding-bottom: 8px; border-bottom: 2px solid #003366;">
        REQUEST DETAILS
    </h3>
    
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #faf5ff; border-radius: 8px; border: 1px solid #d6bcfa;">
        {get_info_row_html("Project", project_title)}
        {get_info_row_html("Heading", log_heading)}
        {get_info_row_html("Session", session)}
    </table>
    
    <!-- Description Box -->
    <div style="background-color: #f8fafc; border-radius: 8px; border: 1px solid #e9ecef; padding: 15px 20px; margin-top: 15px;">
        <p style="color: #666666; font-size: 13px; font-weight: 600; margin: 0 0 8px 0;">Description:</p>
        <p style="color: #333333; font-size: 14px; line-height: 1.6; margin: 0; white-space: pre-wrap;">{desc_display}</p>
    </div>
    """
    return content


def get_log_submission_plain_text(user_name, emp_id, log_date, project_title, log_heading, session, description):
    """Generate plain text content for log submission email"""
    return f"""
Greetings of the day,

Hai Team,

Please find the information submitted by the user.

User Name    : {user_name}
Employee ID  : {emp_id}
Date         : {log_date}

REQUEST DETAILS:
----------------
Project      : {project_title}
Heading      : {log_heading}
Session      : {session}
Description  : 
{description}

----------------------------------------

Thanks & Regards,
TESLEAD IT TEAM
"""


# ============================================
# MAIN EMAIL SENDING FUNCTIONS
# ============================================

def send_admin_notification(subject, html_body, text_body, title="Notification"):
    """
    Send email notification to admin.
    
    Args:
        subject: Email subject line
        html_body: HTML content for the email body
        text_body: Plain text content for the email body
        title: Title for the email header
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        from_email = settings.EMAIL_HOST_USER
        admin_email = getattr(settings, 'ADMIN_EMAIL', settings.EMAIL_HOST_USER)
        
        # Wrap content in base template
        full_html = get_base_html_template(title, html_body)
        
        # Create email with both HTML and plain text
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=from_email,
            to=[admin_email]
        )
        
        email.attach_alternative(full_html, "text/html")
        email.send(fail_silently=False)
        
        return True, "Notification sent successfully"
        
    except Exception as e:
        logger.error(f"Failed to send admin notification: {str(e)}")
        return False, f"Failed to send notification: {str(e)}"


def send_leave_request_notification(user_name, emp_id, leave_date, leave_type, notes=""):
    """
    Send leave request notification to admin.
    
    Args:
        user_name: Employee name
        emp_id: Employee ID
        leave_date: Date of leave (formatted string)
        leave_type: Type of leave (Planned/Casual/Emergency/Sick)
        notes: Additional notes
    
    Returns:
        tuple: (success: bool, message: str)
    """
    today = datetime.now().strftime('%d %b %Y')
    subject = f"Leave Request - {user_name} - {today}"
    
    html_body = get_leave_request_html(user_name, emp_id, leave_date, leave_type, notes)
    text_body = get_leave_request_plain_text(user_name, emp_id, leave_date, leave_type, notes)
    
    return send_admin_notification(subject, html_body, text_body, "Leave Request")


def send_wfh_request_notification(user_name, emp_id, wfh_date, reason, notes=""):
    """
    Send WFH request notification to admin.
    
    Args:
        user_name: Employee name
        emp_id: Employee ID
        wfh_date: Date of WFH (formatted string)
        reason: Reason for WFH
        notes: Additional notes
    
    Returns:
        tuple: (success: bool, message: str)
    """
    today = datetime.now().strftime('%d %b %Y')
    subject = f"Work From Home Request - {user_name} - {today}"
    
    html_body = get_wfh_request_html(user_name, emp_id, wfh_date, reason, notes)
    text_body = get_wfh_request_plain_text(user_name, emp_id, wfh_date, reason, notes)
    
    return send_admin_notification(subject, html_body, text_body, "Work From Home Request")


def send_compoff_request_notification(user_name, emp_id, sunday_date, work_purpose, compoff_date, notes=""):
    """
    Send comp-off request notification to admin.
    
    Args:
        user_name: Employee name
        emp_id: Employee ID
        sunday_date: Sunday worked on (formatted string)
        work_purpose: Purpose of Sunday work
        compoff_date: Requested comp-off date (or None)
        notes: Additional notes
    
    Returns:
        tuple: (success: bool, message: str)
    """
    today = datetime.now().strftime('%d %b %Y')
    subject = f"Comp-Off Request - {user_name} - {today}"
    
    html_body = get_compoff_request_html(
        user_name, emp_id, today, sunday_date, work_purpose, compoff_date, notes
    )
    text_body = get_compoff_request_plain_text(
        user_name, emp_id, today, sunday_date, work_purpose, compoff_date, notes
    )
    
    return send_admin_notification(subject, html_body, text_body, "Comp-Off Request")


def send_log_submission_notification(user_name, emp_id, log_date, project_title, log_heading, session, description):
    """
    Send log submission notification to admin.
    
    Args:
        user_name: Employee name
        emp_id: Employee ID
        log_date: Date of log (formatted string)
        project_title: Project name
        log_heading: Log heading/title
        session: Session type (First Half/Second Half)
        description: Log details/description
    
    Returns:
        tuple: (success: bool, message: str)
    """
    today = datetime.now().strftime('%d %b %Y')
    subject = f"New Log Submitted - {user_name} - {today}"
    
    html_body = get_log_submission_html(
        user_name, emp_id, log_date, project_title, log_heading, session, description
    )
    text_body = get_log_submission_plain_text(
        user_name, emp_id, log_date, project_title, log_heading, session, description
    )
    
    return send_admin_notification(subject, html_body, text_body, "New Log Submission")
