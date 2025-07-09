from django.conf import settings
from loguru import logger
import resend


def send_email_with_resend(to, subject, html_content):
    """Send email using Resend API"""
    try:
        resend.api_key = settings.RESEND_API_KEY

        params = {
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [to],
            "subject": subject,
            "html": html_content,
        }

        # Send the email
        response = resend.Emails.send(params)
        return True, response
    except Exception as e:
        # Log the error and fall back to console
        print(f"Resend email error: {str(e)}")
        print(f"Email to: {to}")
        print(f"Subject: {subject}")
        print(f"Content: {html_content}")
        return False, str(e)


def send_welcome_email(user):
    """Send a welcome email to a newly registered user."""

    subject = "Welcome to pollution predictions system"

    html_content = """
    <html>
    <body>
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 5px;">
            <h2 style="color: #2c3e50;">Welcome to Pollution Prediction System</h2>
            <p>Hello,</p>
            <p>Thank you for registering with our Pollution Prediction System. We're excited to have you on board!</p>
            <p>With your account, you can:</p>
            <ul>
                <li>Access real-time pollution and weather data</li>
                <li>Receive alerts when pollution levels exceed your threshold</li>
                <li>View predictions for future pollution levels</li>
            </ul>
            <p>If you have any questions, please don't hesitate to contact us.</p>
            <p>Best regards,<br>The Pollution Prediction Team</p>
    </body>
    </html>
        """

    
    logger.info(f"Welcome email sent to {user.email}")
    return  send_email_with_resend(user.email, subject, html_content)



def send_password_reset_email(user, token):
    """Send a password reset email to a user."""

    subject = "Reset your password"

    
    html_content = f"""
      <html>
    <body>
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 5px;">
            <h2 style="color: #2c3e50;">Reset Your Password</h2>
            <p>Hello,</p>
            <p>We received a request to reset your password. If you didn't make this request, you can ignore this email.</p>
            <p>To reset your password, please click the button below:</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="/reset-password?token={token}" style="background-color: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">Reset Password</a>
            </div>
            <p>This link will expire in 24 hours.</p>
            <p>Best regards,<br>The Pollution Prediction Team</p>
        </div>
            </body>
    </html>
        """
    
    logger.info(f"Password reset email sent to {user.email}")
    return send_email_with_resend(user.email, subject, html_content)


def send_pollution_alert_email(user, data):
    """Send an alert email when pollution exceeds the user's threshold."""
    
    location = data.get('location', 'your area')
    pollutant = data.get('pollutant', 'PM2.5')
    value = data.get('value', 'high')
    time = data.get('time', 'now')

    subject = f"⚠️ Pollution Alert: High {pollutant} Levels Detected"
    
    html_content = f"""
       <html>
    <body>
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 5px;">
            <h2 style="color: #e74c3c;">⚠️ Pollution Alert</h2>
            <p>Hello,</p>
            <p>We're alerting you that pollution levels in {location} have exceeded your set threshold.</p>
            <div style="background-color: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 15px; border-radius: 5px; margin: 15px 0;">
                <p><strong>Alert Details:</strong></p>
                <ul>
                    <li><strong>Pollutant:</strong> {pollutant}</li>
                    <li><strong>Current Value:</strong> {value}</li>
                    <li><strong>Threshold:</strong> {user.pollution_threshold}</li>
                    <li><strong>Time:</strong> {time}</li>
                    <li><strong>Location:</strong> {location}</li>
                </ul>
            </div>
            <p><strong>Health Recommendations:</strong></p>
            <ul>
                <li>Consider limiting outdoor activities</li>
                <li>Keep windows closed</li>
                <li>Use air purifiers if available</li>
                <li>Stay hydrated</li>
            </ul>
            <p>You can adjust your alert threshold in your account settings.</p>
            <p>Stay safe,<br>The Pollution Prediction Team</p>
        </div>
           </body>
    </html>
        """
    logger.info(f"Pollution alert email sent to {user.email}")
    return send_email_with_resend(user.email, subject, html_content)