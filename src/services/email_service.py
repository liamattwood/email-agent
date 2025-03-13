import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

def send_email(recipient: str, subject: str, body: str) -> dict:
    try:
        gmail_user = os.getenv('GMAIL_USER')
        gmail_password = os.getenv('GMAIL_APP_PASSWORD')
        
        if not gmail_user or not gmail_password:
            return {"error": "Gmail credentials not found in environment variables. Set GMAIL_USER and GMAIL_APP_PASSWORD."}
        
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = recipient
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.set_debuglevel(0)
        
        try:
            server.login(gmail_user, gmail_password)
        except smtplib.SMTPAuthenticationError as auth_error:
            server.quit()
            if "Username and Password not accepted" in str(auth_error):
                return {
                    "error": "Authentication failed. Please check that:\n"
                            "1. Your Gmail account has 2-Step Verification enabled\n"
                            "2. You're using an App Password (not your regular password)\n"
                            "3. The App Password is correct and has no extra spaces\n"
                            "4. If you can't access App Passwords, you may need to use a regular password with 'Less secure app access' enabled"
                }
            return {"error": f"SMTP Authentication Error: {str(auth_error)}"}
        
        server.send_message(msg)
        server.quit()
        
        return {
            "status": "success",
            "message": f"Email sent to {recipient}",
            "details": {
                "recipient": recipient,
                "subject": subject
            }
        }
    except Exception as e:
        return {"error": f"Failed to send email: {str(e)}"} 