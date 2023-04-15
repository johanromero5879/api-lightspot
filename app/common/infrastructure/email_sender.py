from enum import StrEnum
from smtplib import SMTP

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Body(StrEnum):
    PLAIN = "plain"
    HTML = "html"


class SendEmail:

    @property
    def port(self):
        return 587

    def __init__(self, server: str, username: str, password: str):
        self.server = server
        self.__username = username
        self.__password = password

    def __call__(self, subject: str, body: str, to: str, body_type: Body = Body.PLAIN):
        # Create a MIME multipart message
        msg = MIMEMultipart()
        msg["Subject"] = subject

        # Create body
        msg.attach(MIMEText(body, body_type))

        # Create notes
        note = "<br><br><i>Este correo es autogenerado, por favor no responda a este.</i>"
        msg.attach(MIMEText(note, Body.HTML))

        try:
            # Connect to SMTP server and send email
            with SMTP(self.server, self.port) as server:
                server.starttls()
                server.login(self.__username, self.__password)

                server.sendmail(self.__username, to, msg.as_string())
        except Exception:
            raise EmailError()


class EmailError(Exception):
    def __init__(self):
        message = "Error on email sender"
        super().__init__(message)
