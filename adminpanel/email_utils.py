"""
Email Utility Module for TESLEAD IT Team
Handles welcome emails and other email notifications using Django's email system.
"""

import string
import secrets
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def generate_temp_password(length=10):
    """
    Generate a secure random temporary password.
    Contains uppercase, lowercase, digits, and special characters.
    """
    alphabet = string.ascii_letters + string.digits + "!@#$%&*"
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password


def get_welcome_email_html(user_name, username, temp_password):
    """
    Generate professional HTML email template for welcome email.
    Clean, corporate design with TESLEAD branding.
    """
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to TESLEAD IT Team</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #f4f6f9; padding: 40px 20px;">
        <tr>
            <td align="center">
                <table role="presentation" width="600" cellspacing="0" cellpadding="0" style="background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); overflow: hidden;">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #003366 0%, #004d99 100%); padding: 30px 40px; text-align: center;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 600; letter-spacing: 1px;">
                                TESLEAD IT TEAM
                            </h1>
                            <p style="color: #b3d4fc; margin: 8px 0 0 0; font-size: 14px;">
                                Welcome Aboard!
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Body Content -->
                    <tr>
                        <td style="padding: 40px;">
                            <p style="color: #333333; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                                Hi <strong>{user_name}</strong>,
                            </p>
                            
                            <p style="color: #555555; font-size: 15px; line-height: 1.7; margin: 0 0 25px 0;">
                                Welcome to our <strong>TESLEAD IT team</strong>! Your account has been successfully created.
                            </p>
                            
                            <p style="color: #555555; font-size: 15px; line-height: 1.7; margin: 0 0 15px 0;">
                                Below are your login credentials:
                            </p>
                            
                            <!-- Credentials Box -->
                            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #f8fafc; border-radius: 8px; border-left: 4px solid #003366; margin: 20px 0;">
                                <tr>
                                    <td style="padding: 20px 25px;">
                                        <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
                                            <tr>
                                                <td style="padding: 8px 0;">
                                                    <span style="color: #666666; font-size: 14px;">Username:</span>
                                                    <span style="color: #003366; font-size: 15px; font-weight: 600; margin-left: 10px;">{username}</span>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 8px 0;">
                                                    <span style="color: #666666; font-size: 14px;">Temporary Password:</span>
                                                    <span style="color: #003366; font-size: 15px; font-weight: 600; margin-left: 10px; font-family: 'Courier New', monospace; background-color: #e8f0fe; padding: 4px 10px; border-radius: 4px;">{temp_password}</span>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Important Notice -->
                            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #fff8e6; border-radius: 8px; border: 1px solid #ffd966; margin: 25px 0;">
                                <tr>
                                    <td style="padding: 18px 20px;">
                                        <p style="color: #856404; font-size: 14px; margin: 0 0 10px 0; font-weight: 600;">
                                            🔐 IMPORTANT:
                                        </p>
                                        <p style="color: #856404; font-size: 14px; margin: 0; line-height: 1.6;">
                                            You must change your password during your first login.
                                        </p>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Time Notice -->
                            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #e8f4fd; border-radius: 8px; border: 1px solid #b3d7f5; margin: 20px 0;">
                                <tr>
                                    <td style="padding: 18px 20px;">
                                        <p style="color: #0c5460; font-size: 14px; margin: 0 0 10px 0; font-weight: 600;">
                                            ⏳ NOTE:
                                        </p>
                                        <p style="color: #0c5460; font-size: 14px; margin: 0; line-height: 1.6;">
                                            Your temporary password is valid only for the next <strong>24 hours</strong>.<br>
                                            Please log in soon and update your password.
                                        </p>
                                    </td>
                                </tr>
                            </table>
                            
                            <p style="color: #555555; font-size: 14px; line-height: 1.7; margin: 25px 0 0 0;">
                                If you face any issues, feel free to contact the IT support team.
                            </p>
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
                                This is an automated message. Please do not reply to this email.
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
    return html_content


def get_welcome_email_plain_text(user_name, username, temp_password):
    """
    Generate plain text version of welcome email.
    """
    plain_text = f"""
Hi {user_name},

Welcome to our TESLEAD IT team!

Your account has been successfully created.

Below are your login credentials:

Username: {username}
Temporary Password: {temp_password}

----------------------------------------

🔐 IMPORTANT:
You must change your password during your first login.

⏳ NOTE:
Your temporary password is valid only for the next 24 hours.
Please log in soon and update your password.

----------------------------------------

If you face any issues, feel free to contact the IT support team.

Thanks & Regards,
TESLEAD IT TEAM

---
This is an automated message. Please do not reply to this email.
"""
    return plain_text


def send_welcome_email(user_email, user_name, username, temp_password):
    """
    Send welcome email to newly created user.
    
    Args:
        user_email: Recipient's email address
        user_name: User's display name
        username: Login username (EMP_ID or EMAIL)
        temp_password: Generated temporary password
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        subject = "Welcome to TESLEAD IT Team – Your Account Details"
        from_email = settings.EMAIL_HOST_USER
        to_email = [user_email]
        
        # Generate email content
        html_content = get_welcome_email_html(user_name, username, temp_password)
        plain_text_content = get_welcome_email_plain_text(user_name, username, temp_password)
        
        # Create email with both HTML and plain text versions
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_text_content,
            from_email=from_email,
            to=to_email
        )
        
        # Attach HTML version
        email.attach_alternative(html_content, "text/html")
        
        # Send email
        email.send(fail_silently=False)
        
        return True, "Welcome email sent successfully"
        
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"


def send_password_reset_email(user_email, user_name, username, temp_password):
    """
    Send password reset email when admin resets a user's password.
    
    Args:
        user_email: Recipient's email address
        user_name: User's display name
        username: Login username (EMP_ID or EMAIL)
        temp_password: New temporary password
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        subject = "TESLEAD IT Team – Password Reset Notification"
        from_email = settings.EMAIL_HOST_USER
        to_email = [user_email]
        
        # Reuse welcome email template with slight modification
        html_content = get_welcome_email_html(user_name, username, temp_password)
        html_content = html_content.replace(
            "Welcome Aboard!",
            "Password Reset"
        ).replace(
            "Your account has been successfully created.",
            "Your password has been reset by the administrator."
        )
        
        plain_text_content = get_welcome_email_plain_text(user_name, username, temp_password)
        plain_text_content = plain_text_content.replace(
            "Your account has been successfully created.",
            "Your password has been reset by the administrator."
        )
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_text_content,
            from_email=from_email,
            to=to_email
        )
        
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        
        return True, "Password reset email sent successfully"
        
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"
