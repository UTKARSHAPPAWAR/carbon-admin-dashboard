import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

def send_otp(recipient_email, username, otp):
    """
    Sends a 6-digit OTP to the specified email address using Gmail SMTP.
    """
    # Load and check credentials
    load_dotenv()
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASS")

    if not user or not isinstance(user, str):
        print("ERROR: SMTP_USER not found or not a valid string in environment.")
        return False
    if not password or not isinstance(password, str):
        print("ERROR: SMTP_PASS not found or not a valid string in environment.")
        return False

    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = f"Carbon Footprint Navigator <{user}>"
        msg['To'] = recipient_email
        msg['Subject'] = "Your Verification Code - Carbon Footprint Navigator"

        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px; color: #333;">
            <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; border-radius: 10px; padding: 20px;">
                <h2 style="color: #2a5298;">Hello {username},</h2>
                <p>Your 6-digit verification code for Carbon Footprint Navigator is:</p>
                <div style="background: #f4f4f4; border-radius: 8px; padding: 15px; text-align: center; margin: 20px 0;">
                    <h1 style="color: #2a5298; font-size: 32px; letter-spacing: 5px; margin: 0;">{otp}</h1>
                </div>
                <p>This code will expire in 10 minutes. Please do not share this code with anyone.</p>
                <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="font-size: 12px; color: #777;">Best regards,<br>The Carbon Footprint Team</p>
            </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        # Connect and send
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(user, password)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"ERROR: Failed to send email: {e}")
        return False
