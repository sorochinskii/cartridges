import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTPRecipientsRefused
from typing import Any, Dict, Optional

from config import settings
from cryptography.fernet import Fernet
from jinja2 import Environment, FileSystemLoader
from loguru import logger
from smtp_exceptions_handler import SMTPExceptionsHandler


class EmailService:
    """Сервис для отправки email сообщений"""

    def __init__(self, user_email: str):
        self.sender = EmailSender(
            smtp_server=settings.SMTP_SERVER,
            smtp_port=settings.SMTP_PORT,
            sender=settings.SENDER_EMAIL,
            sender_password=settings.SENDER_PASSWORD,
            recipient=user_email,
        )
        self.user_email = user_email

    def send_verification_email(self, token: str) -> None:
        """Отправка email для верификации"""
        fernet = Fernet(settings.VERIFY_TOKEN_SECRET.encode())
        enc_token = fernet.encrypt(token.encode())

        message = self._render_email_message(
            template=settings.TEMPLATE_VERIFICATION,
            subject="Verification message",
            token=enc_token.decode(),
            url=self._build_frontend_url(settings.FRONTEND_VERIFY_PATH),
        )

        self._send_email(message)

    def send_password_reset_email(self, token: str) -> None:
        message = self._render_email_message(
            template=settings.TEMPLATE_VERIFICATION,
            subject="Password reset",
            token=token,
        )

        self._send_email(message)

    def send_registration_email(self) -> None:
        message = self._render_email_message(
            template="email_registration.html",
            subject="Registration message",
            url=self._build_frontend_url(settings.FRONTEND_LOGIN_PATH),
        )

        try:
            self._send_email(message)
        except SMTPRecipientsRefused as ex:
            logger.error(f"Failed to send registration email: {ex}")

    def _render_email_message(self, **kwargs) -> str:
        renderer = EmailMessageRenderer(
            templates_dir=settings.TEMPLATES_DIR,
            template_name=kwargs.get("template"),
        )
        return renderer.render_message(
            subject=kwargs.get("subject"),
            url=kwargs.get("url"),
            token=kwargs.get("token"),
            sender=settings.SENDER_EMAIL,
            recepient=self.user_email,
        )

    def _build_frontend_url(self, path: str) -> str:
        return URLBuilder(
            settings.HTTP_SECURE,
            settings.FRONTEND_HOST,
            settings.FRONTEND_PORT,
            [path],
        ).url()

    def _send_email(self, message: str) -> None:
        with SMTPExceptionsHandler():
            self.sender.send(message=message)


class URLBuilder:
    def __init__(
        self,
        protocol: str,
        host: str,
        port: str | int | None = None,
        path: list[str] | None = None,
    ):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.path = path or []

    def _path(self) -> str:
        match len(self.path):
            case 0:
                return ""
            case _:
                if self.path[-1][-1] != "/":
                    return "/".join(self.path) + "/"
                else:
                    return "/".join(self.path)

    def _semicoloned_port(self) -> str | None:
        if self.port:
            return ":" + str(self.port)
        else:
            return str(self.port)

    def url(self):
        url_list = [
            self.protocol,
            "://",
            self.host,
            self._semicoloned_port(),
            "/",
            self._path(),
        ]
        url = "".join(url_list)
        return url


class EmailSender:
    """Класс для отправки электронных писем через SMTP с SSL."""

    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        sender: str,
        sender_password: str,
        recipient: str,
    ):
        """
        Инициализация отправителя email.

        :param smtp_server: SMTP сервер
        :param smtp_port: Порт SMTP сервера
        :param sender: Email отправителя
        :param sender_password: Пароль отправителя
        :param recipient: Email получателя
        """
        self.smtp_server = smtp_server
        self.port = smtp_port
        self.sender = sender
        self.sender_password = sender_password
        self.recipient = recipient
        self.ssl_context = ssl.create_default_context()

    def send(self, message: str = "") -> None:
        """
        Отправка email сообщения.

        :param message: Строка с содержимым сообщения
        :raises smtplib.SMTPException: При ошибках отправки
        """
        with smtplib.SMTP_SSL(
            self.smtp_server, self.port, context=self.ssl_context
        ) as server:
            server.login(self.sender, self.sender_password)
            server.sendmail(self.sender, self.recipient, message)


class EmailMessageRenderer:
    def __init__(
        self,
        templates_dir: str,
        template_name: str,
    ):
        """
        Инициализация рендерера сообщений.

        :param templates_dir: Директория с шаблонами
        :param template_name: Имя файла шаблона
        """
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        self.template = self.env.get_template(template_name)
        self.last_render_kwargs: Optional[Dict[str, Any]] = None

    def render_message(
        self,
        subject: str = "",
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        **template_vars: Any,
    ) -> str:
        """
        Рендеринг email сообщения из шаблона.

        :param subject: Тема письма
        :param sender: Email отправителя
        :param recipient: Email получателя
        :param template_vars: Переменные для шаблона
        :return: Строка с готовым сообщением
        """
        self.last_render_kwargs = template_vars
        html_content = self.template.render(**template_vars)
        message = MIMEMultipart()
        if sender:
            message["From"] = sender
        if recipient:
            message["To"] = recipient
        message["Subject"] = subject
        message.attach(MIMEText(html_content, "html"))
        return message.as_string()
