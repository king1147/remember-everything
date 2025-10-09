import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class EmailSender:
    def __init__(self, config):
        self.config = config

    def send_email(self, message_content):
        """Send email with the message content"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.config['EMAIL_FROM']
            msg['To'] = self.config['EMAIL_TO']
            msg['Subject'] = f'Message from RabbitMQ'

            # Email body
            body = f"""

            {message_content}

            ---
            This is an automated message from the Mail Sender Service.
            """

            msg.attach(MIMEText(body, 'plain'))

            # Connect to SMTP server
            server = smtplib.SMTP(self.config['SMTP_SERVER'], self.config['SMTP_PORT'])

            if self.config['SMTP_USE_TLS']:
                server.starttls()

            # Login
            server.login(self.config['SMTP_USERNAME'], self.config['SMTP_PASSWORD'])

            # Send email
            server.send_message(msg)
            server.quit()

            logger.info(f"Email sent successfully: {message_content[:50]}...")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
