"""Module email  """

import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os


class Emailer:
    """Class representing"""

    def __init__(self, abs_config_path: str, abs_texvars_path: str):
        # Load config from file
        with open(abs_config_path, 'r', encoding='utf8') as file:
            self.config = json.load(file)['mailer']
        with open(abs_texvars_path, 'r', encoding='utf8') as file:
            self.tex = json.load(file)
        # Generate message obj
        self.message = MIMEMultipart()
        self.message['From'] = self.config['sender_email']
        self.message['To'] = self.tex['theirEmailAddress']
        self.message['Subject'] = f"Application for {self.tex['vacancyTitle'].strip()}; Vacancy {self.tex['vacancyID']}"
        # Build body
        # TODO: Set greeting based on time of application!
        self.greeting = f"Good afternoon {self.tex['hiringManager']}:\n\n"
        self.info = f"I am writing to apply for the {self.tex['vacancyTitle'].strip()} position; vacancy {self.tex['vacancyID']}.\nAttached: resume, cover letter\n\n"
        self.closing = f"Thank you for the consideration, \nNicholas J. Kammerer\n <{self.config['sender_email']}>"
        self.body = self.greeting + self.info + self.closing
        # Add body to message
        self.message.attach(MIMEText(self.body, 'plain'))
        # Add PDF attachments
        for pdf in self.config['attachments']:
            attachment = MIMEApplication(
                open(pdf, "rb").read(), _subtype="pdf")
            attachment.add_header('Content-Disposition',
                                  'attachment', filename=os.path.basename(pdf))
            self.message.attach(attachment)

    def send_email(self) -> None:
        """Tries to connect to a class-defined SMTP server. If unsuccessful, return error."""
        try:  # self.config['smtp_server_address']
            with smtplib.SMTP(self.config['smtp_server_address'], self.config['smtp_port']) as svr:
                print("Server allowed access... sending mail...")
                svr.starttls()
                svr.login(self.config['sender_email'],
                          self.config['sender_password'])
                svr.send_message(self.message)
            print(f"Message sent to {self.message['To']}")
        except Exception as e:
            print("Server denied access...\n")
            print(f"Error sending email: {e}")
