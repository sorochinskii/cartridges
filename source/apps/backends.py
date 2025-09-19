from typing import Callable

from config import settings
from fastapi import Request, Response
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    CookieTransport,
    JWTStrategy,
    Strategy,
)
from fastapi_users.authentication.transport import Transport

bearer_transport = BearerTransport(tokenUrl="/v1/auth/jwt/login")

cookie_transport = CookieTransport(
    cookie_name=settings.COOKIE_NAME,
    cookie_max_age=settings.REFRESH_TOKEN_LIFETIME,
    cookie_httponly=True,
    cookie_secure=True,
    cookie_samesite="lax",
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.JWT_SECRET,
        lifetime_seconds=settings.TOKEN_LIFETIME,
        token_audience=["cartridges"],
    )


class RefreshTokenTransport:
    async def get_token(self, request: Request) -> str | None:
        return request.cookies.get(settings.COOKIE_NAME)

    async def get_refresh_token(self, request: Request) -> str | None:
        return request.cookies.get(f"{settings.COOKIE_NAME}")

    def set_cookies(self, response: Response, refresh_token: str):
        response.set_cookie(
            key=settings.COOKIE_NAME,
            value=refresh_token,
            secure=False,
            httponly=True,
            samesite="lax",
        )

    def delete_cookies(self, response: Response):
        response.delete_cookie(settings.COOKIE_NAME)
        response.delete_cookie(f"{settings.COOKIE_NAME}")


class RefreshAuthBackend(AuthenticationBackend):
    def __init__(
        self,
        name: str,
        transport: Transport,
        get_strategy: Callable[[], Strategy],
        refresh_transport: RefreshTokenTransport,
    ):
        self.refresh_transport = refresh_transport
        super().__init__(
            name=name, transport=transport, get_strategy=get_strategy
        )


def get_auth_backend():
    bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
    refresh_transport = RefreshTokenTransport()

    return RefreshAuthBackend(
        name="jwt",
        transport=bearer_transport,
        get_strategy=get_jwt_strategy,
        refresh_transport=refresh_transport,
    )
