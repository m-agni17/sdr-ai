# send a sample mail using python and smtp

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email.mime.application import MIMEApplication

def send_email(sender_email, recipient_email, subject, body, smtp_server, smtp_port, smtp_user, smtp_password):
    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = formataddr(('Sender Name', sender_email))
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Attach the email body
        msg.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(smtp_user, smtp_password)  # Login to the server
            server.send_message(msg)  # Send the email

        return {"status": "success", "message": "Email sent successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

# Send a sample email
sender_email = ""
recipient_email = ""
subject = "Test Email"
body = "This is a test email sent using Python and SMTP."
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_user = "your_smtp_user"
smtp_password = "your_smtp_password"


result = send_email(sender_email, recipient_email, subject, body, smtp_server, smtp_port, smtp_user, smtp_password)
print(result)


# Output: {'status': 'success', 'message': 'Email sent successfully'}

# The email should be sent successfully if the SMTP server, port, user, and password are correct.

# Note: Make sure to enable "Less secure app access" in your Gmail account settings to send emails using SMTP.