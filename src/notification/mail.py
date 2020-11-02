from notification.notification import Notification
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email(Notification):
    def __init__(self, loggers, smtp_server_address, smtp_server_port, email_from, passwd, email_to):
        """
        Parameters
        ----------
        loggers: list
            list of loggers to send
        smtp_server_address: str
            address of smtp server
        smtp_server_port: int
            port of smtp server
        email_from: str
            login on the smtp server
        passwd: str
            password of the smtp server
        email_to: str
            send logs to email_to
        """
        Notification.__init__(self, loggers)
        self.__email_from = email_from
        self.__email_to = email_to
        self.__smtp_server = smtplib.SMTP(host=smtp_server_address, port=smtp_server_port)
        self.__smtp_server.starttls()
        self.__smtp_server.login(email_from, passwd)

    def _send(self, text):
        msg = MIMEMultipart()

        msg['From'] = self.__email_from
        msg['To'] = self.__email_to
        msg['Subject'] = 'TEST INFO'

        msg.attach(MIMEText(text, 'plain'))
        self.__smtp_server.send_message(msg)

        del msg
        return True

    def __del__(self):
        self.__smtp_server.quit()
