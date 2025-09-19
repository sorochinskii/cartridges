import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, FileSystemLoader


class EmailSender:
    def __init__(self,
                 smtp_server: str,
                 smtp_port: int,
                 sender: str,
                 sender_password: str,
                 recepient: str,
                 ):
        self.port = smtp_port
        self.smtp_server = smtp_server
        self.sender = sender
        self.sender_password = sender_password
        self.recepient = recepient

    def send(self, message: str = ''):
        SSL_context = ssl.create_default_context()
        with smtplib.SMTP_SSL(
                self.smtp_server, self.port, context=SSL_context) as server:
            server.login(self.sender, self.sender_password)
            server.sendmail(self.sender, self.recepient, message)


class RenderEmailMessage:
    def __init__(self,
                 templates_dir: str,
                 template: str,
                 * args, **kwargs
                 ):
        env = Environment(
            loader=FileSystemLoader(templates_dir)
        )
        self._kwargs = None
        self.template = env.get_template(template)

    def message(self, subject: str = '', *args, **kwargs):
        self._kwargs = kwargs
        from_addr = self._kwargs.get('sender')
        to_addr = self._kwargs.get('recepient')
        rendered_page = self.template.render(**kwargs)
        message = MIMEMultipart()
        message['From'] = from_addr
        message['To'] = to_addr
        message['Subject'] = subject
        message.attach(MIMEText(rendered_page, "html"))
        return message.as_string()

    def get_kwargs(self):
        return self._kwargs


class URLBuilder:

    def __init__(self,
                 protocol: str,
                 host: str,
                 port: str | int | None = None,
                 *args, **kwargs):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.args = args
