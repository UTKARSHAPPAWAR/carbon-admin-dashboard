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
    if not isinstance(SMTP_USER, str) or not isinstance(SMTP_PASS, str):
        print("ERROR: SMTP credentials must be strings. Check your .env file.")
        return False

    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = f"Carbon Footprint Navigator <{SMTP_USER}>"
        msg['To'] = recipient_email
        msg['Subject'] = "Your Verification Code - Carbon Footprint Navigator"

        body = f"""
        <html>
        <body>
            <h2>Hello {username},</h2>
            <p>Your 6-digit verification code for Carbon Footprint Navigator is:</p>
            <h1 style="color: #2a5298; font-size: 32px; letter-spacing: 5px;">{otp}</h1>
            <p>This code will expire in 10 minutes. Please do not share this code with anyone.</p>
            <br>
            <p>Best regards,<br>The Carbon Footprint Team</p>
        </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        # Connect to Gmail SMTP server
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(SMTP_USER, SMTP_PASS)
        
        # Send the email
        text = msg.as_string()
        server.sendmail(SMTP_USER, recipient_email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"ERROR: Failed to send email: {e}")
        return False
