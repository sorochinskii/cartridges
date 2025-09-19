import jwt
from apps.backends import (
    cookie_transport,
    get_auth_backend,
)
from apps.utils import EmailService
from config import settings
from cryptography.fernet import Fernet
from db.db import get_async_session
from db.models.users import User
from fastapi import Depends, Request, Response
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    InvalidPasswordException,
    UUIDIDMixin,
    exceptions,
    models,
)
from fastapi_users.db import BaseUserDatabase
from fastapi_users.jwt import decode_jwt
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from http_exceptions import HTTPObjectNotExist
from schemas.users_base import UserBaseSchema
from sqlalchemy.ext.asyncio import AsyncSession


class UserManager(UUIDIDMixin, BaseUserManager):
    reset_password_token_secret = settings.JWT_SECRET
    verification_token_secret = settings.JWT_SECRET

    def __init__(self, user_db: BaseUserDatabase):
        super().__init__(user_db)

    async def on_after_register(
        self, user: User, request: Request | None = None
    ) -> None:
        email_service = EmailService(user.email)
        email_service.send_registration_email()

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ) -> None:
        if not token:
            raise HTTPObjectNotExist

        email_service = EmailService(user.email)
        email_service.send_password_reset_email(token)

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ) -> None:
        if not token:
            raise HTTPObjectNotExist

        email_service = EmailService(user.email)
        email_service.send_verification_email(token)

    async def validate_password(
        self,
        password: str,
        user: UserBaseSchema,
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password should not contain e-mail"
            )

    async def on_after_login(
        self,
        user: User,
        request: Request | None = None,
        response: Response | None = None,
    ) -> None:
        if response:
            strategy = await get_refresh_strategy()
            token = await strategy.write_token(user)
            await cookie_transport.get_login_response(token)

    async def verify(
        self, enc_token: str, request: Request | None = None
    ) -> models.UP:
        fernet = Fernet(settings.VERIFY_TOKEN_SECRET)
        token = fernet.decrypt(enc_token).decode()

        try:
            data = decode_jwt(
                token,
                self.verification_token_secret,
                [self.verification_token_audience],
            )
            user_id = data["sub"]
            email = data["email"]

            user = await self.get_by_email(email)
            if self.parse_id(user_id) != user.id:
                raise exceptions.InvalidVerifyToken()

            if user.is_verified:
                raise exceptions.UserAlreadyVerified()

            verified_user = await self._update(user, {"is_verified": True})
            await self.on_after_verify(verified_user, request)

            return verified_user

        except (
            jwt.PyJWTError,
            KeyError,
            exceptions.UserNotExists,
            exceptions.InvalidID,
        ):
            raise exceptions.InvalidVerifyToken()


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
):
    yield UserManager(user_db)


def get_fastapi_users(user_manager: BaseUserManager) -> FastAPIUsers:
    backend = get_auth_backend()
    return FastAPIUsers(get_user_manager, [backend])


fastapi_users = get_fastapi_users(get_user_manager)
