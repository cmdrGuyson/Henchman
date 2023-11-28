import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from utils.logger import Logger

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")


class EmailModule:
    """Responsible for managing and sending emails"""

    def __init__(
        self,
    ):
        self.message = MIMEMultipart()
        self.message["From"] = GMAIL_USER
        self.logger = Logger(EmailModule.__name__)

    def attach_image(self, path, cid):
        self.logger.info(f"Attaching image. cid: {cid}. path: {path}")
        with open(path, "rb") as image_file:
            image = MIMEImage(image_file.read(), name="image.jpg")
            image.add_header("Content-ID", cid)
            self.message.attach(image)

    def set_html_content(self, html):
        self.logger.info("Setting HTML content")
        html_part = MIMEText(html, "html")
        self.message.attach(html_part)

    def set_subject(self, subject):
        self.message["Subject"] = subject

    def send_email(self, to_email):
        self.logger.info(f"Attempting to send email to: {to_email}")
        self.message["To"] = to_email
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(GMAIL_USER, GMAIL_PASSWORD)

                server.sendmail(
                    GMAIL_USER, self.message.get("To"), self.message.as_string()
                )
                self.logger.info(f"Send email successfully to: {to_email}")
        except Exception as e:
            self.logger.error(f"Something went wrong while sending email. error: {e}")
