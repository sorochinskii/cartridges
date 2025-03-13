from smtplib import SMTPRecipientsRefused

import jwt
from apps.utils import EmailSender, RenderEmailMessage, URLBuilder
from config import settings
from cryptography.fernet import Fernet
from db.db import get_async_session
from db.models.users import User
from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    InvalidPasswordException,
    UUIDIDMixin,
    exceptions,
    models,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.jwt import decode_jwt
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from http_exceptions import HTTPObjectNotExist
from loguru import logger
from schemas.users_base import UserBaseSchema
from smtp_exceptions_handler import SMTPExceptionsHandler
from sqlalchemy.ext.asyncio import AsyncSession


class UserManager(UUIDIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.JWT_SECRET
    verification_token_secret = settings.JWT_SECRET

    async def on_after_register(self, user: User,
                                request: Request | None = None):
        verification_message = RenderEmailMessage(
            templates_dir='source/templates',
            template='email_registration.html')
        url_builder = URLBuilder(
            settings.HTTP_SECURE,
            settings.HOST,
            settings.HTTP_PORT,
            'http://localhost:'
        )
        subject = 'Registration message'
        message = verification_message.message(
            subject=subject,
            url=url_builder.url(),
            sender=settings.SENDER_EMAIL,
            recepient=user.email)

        email = EmailSender(smtp_server=settings.SMTP_SERVER,
                            smtp_port=settings.SMTP_PORT,
                            sender=settings.SENDER_EMAIL,
                            sender_password=settings.SENDER_PASSWORD,
                            recepient=user.email)
        try:
            email.send(message)
        except SMTPRecipientsRefused as ex:
            logger.error(ex)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ):
        if not token:
            raise HTTPObjectNotExist
        verification_message = RenderEmailMessage(
            templates_dir=settings.TEMPLATES_DIR,
            template=settings.TEMPLATE_VERIFICATION)
        subject = 'Password reset'
        message = verification_message.message(
            subject=subject,
            token=token)
        email = EmailSender(smtp_server=settings.SMTP_SERVER,
                            smtp_port=settings.SMTP_PORT,
                            sender=settings.SENDER_EMAIL,
                            sender_password=settings.SENDER_PASSWORD,
                            recepient=user.email)
        with SMTPExceptionsHandler():
            email.send(message=message)

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ):
        if not token:
            raise HTTPObjectNotExist
        fernet = Fernet(settings.VERIFY_TOKEN_SECRET.encode())
        enc_token = fernet.encrypt(token.encode())
        verification_message = RenderEmailMessage(
            templates_dir=settings.TEMPLATES_DIR,
            template=settings.TEMPLATE_VERIFICATION)
        subject = 'Verification message'
        message = verification_message.message(
            subject=subject,
            token=enc_token.decode(),
            sender=settings.SENDER_EMAIL,
            recepient=user.email)

        email = EmailSender(smtp_server=settings.SMTP_SERVER,
                            smtp_port=settings.SMTP_PORT,
                            sender=settings.SENDER_EMAIL,
                            sender_password=settings.SENDER_PASSWORD,
                            recepient=user.email)
        with SMTPExceptionsHandler():
            email.send(message=message)

    async def validate_password(
        self,
        password: str,
        user: UserBaseSchema,
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason='Password should be at least 8 characters'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail'
            )

    async def verify(self,
                     enc_token: str,
                     request: Request | None = None) -> models.UP:

        fernet = Fernet(settings.VERIFY_TOKEN_SECRET)
        token = fernet.decrypt(enc_token).decode()
        try:
            data = decode_jwt(
                token,
                self.verification_token_secret,
                [self.verification_token_audience],
            )
        except jwt.PyJWTError:
            raise exceptions.InvalidVerifyToken()

        try:
            user_id = data["sub"]
            email = data["email"]
        except KeyError:
            raise exceptions.InvalidVerifyToken()

        try:
            user = await self.get_by_email(email)
        except exceptions.UserNotExists:
            raise exceptions.InvalidVerifyToken()

        try:
            parsed_id = self.parse_id(user_id)
        except exceptions.InvalidID:
            raise exceptions.InvalidVerifyToken()

        if parsed_id != user.id:
            raise exceptions.InvalidVerifyToken()

        if user.is_verified:
            raise exceptions.UserAlreadyVerified()

        verified_user = await self._update(user, {"is_verified": True})

        await self.on_after_verify(verified_user, request)

        return verified_user


bearer_transport = BearerTransport(tokenUrl='/v1/users/auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.JWT_SECRET,
                       lifetime_seconds=settings.TOKEN_LIFETIME)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db: SQLAlchemyUserDatabase =
                           Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)


# class RoleChecker:
#     def __init__(self, allowed_roles: list):
#         self.allowed_roles = allowed_roles

#     def __call__(self, user: User = Depends(current_active_user)):
#         if user.role not in self.allowed_roles:
#             logger.debug(
#                 f'User with role {user.role} not in {self.allowed_roles}')
#             raise HTTPException(
#                 status_code=403, detail='Operation not permitted')


# allow_create_resource = RoleChecker(['admin', 'superuser'])
# allow_read_resource = RoleChecker(['user'])
