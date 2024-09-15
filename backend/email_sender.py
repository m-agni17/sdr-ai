import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email.mime.application import MIMEApplication

def send_email(sender_email, recipient_email, subject, body, smtp_server, smtp_port, smtp_user, smtp_password):
    
    try:
        if not body.startswith("Dear"):
            body = body.lstrip().lstrip("Dear").lstrip()
        msg = MIMEMultipart()
        msg['From'] = formataddr(('Analytics Sindhya', sender_email))
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls() 
            server.login(smtp_user, smtp_password) 
            server.send_message(msg) 

        return {"status": "success", "message": "Email sent successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
