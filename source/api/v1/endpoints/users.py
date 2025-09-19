from apps.backends import get_auth_backend
from apps.redis_client import get_redis_client
from apps.user_manager import fastapi_users, get_user_manager
from config import settings
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import models
from fastapi_users.authentication import (
    AuthenticationBackend,
    Authenticator,
    Strategy,
)
from fastapi_users.manager import BaseUserManager, UserManagerDependency
from fastapi_users.openapi import OpenAPIResponseType
from fastapi_users.router.common import ErrorCode, ErrorModel
from schemas.users_base import UserBaseCreateSchema, UserBaseSchema
from utils.jwt_tokens import create_tokens, verify_refresh_token

users_router = APIRouter()

users_router.include_router(
    fastapi_users.get_register_router(
        user_schema=UserBaseSchema, user_create_schema=UserBaseCreateSchema
    ),
    prefix="/auth",
    tags=["auth"],
)

users_router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

users_router.include_router(
    fastapi_users.get_users_router(
        user_schema=UserBaseSchema, user_update_schema=UserBaseSchema
    ),
    tags=["users"],
)


def get_auth_router(
    backend: AuthenticationBackend[models.UP, models.ID],
    user_manager: UserManagerDependency[models.UP, models.ID],
    authenticator: Authenticator[models.UP, models.ID],
    requires_verification: bool = False,
) -> APIRouter:
    router = APIRouter()
    refresh_backend = get_auth_backend()
    login_responses: OpenAPIResponseType = {
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.LOGIN_BAD_CREDENTIALS: {
                            "summary": "Bad credentials or the user is inactive.",
                            "value": {
                                "detail": ErrorCode.LOGIN_BAD_CREDENTIALS
                            },
                        },
                        ErrorCode.LOGIN_USER_NOT_VERIFIED: {
                            "summary": "The user is not verified.",
                            "value": {
                                "detail": ErrorCode.LOGIN_USER_NOT_VERIFIED
                            },
                        },
                    }
                }
            },
        },
        **backend.transport.get_openapi_login_responses_success(),
    }

    logout_responses: OpenAPIResponseType = {
        **{
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Missing token or inactive user."
            }
        },
        **backend.transport.get_openapi_logout_responses_success(),
    }

    @router.post(
        "/login",
        name=f"auth:{backend.name}.login",
        responses=login_responses,
    )
    async def login(
        request: Request,
        response: Response,
        credentials: OAuth2PasswordRequestForm = Depends(),
        user_manager: BaseUserManager[models.UP, models.ID] = Depends(
            get_user_manager
        ),
        strategy: Strategy[models.UP, models.ID] = Depends(
            backend.get_strategy
        ),
    ):
        user = await user_manager.authenticate(credentials)

        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
            )
        if requires_verification and not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.LOGIN_USER_NOT_VERIFIED,
            )
        tokens = await create_tokens(str(user.id))
        refresh_backend.refresh_transport.set_cookies(
            response, tokens[settings.COOKIE_NAME]
        )
        return {"access_token": tokens["access_token"], "token_type": "bearer"}

    @router.post(
        "/refresh",
    )
    async def refresh(
        request: Request,
        response: Response,
        user_manager: BaseUserManager = Depends(get_user_manager),
        redis_client=Depends(get_redis_client),
    ):
        refresh_token = (
            await refresh_backend.refresh_transport.get_refresh_token(request)
        )
        if refresh_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing refresh token",
            )

        token_data = await verify_refresh_token(refresh_token, redis_client)
        user = await user_manager.get(token_data.user_id)

        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user",
            )

        await redis_client.revoke_refresh_token(refresh_token)

        tokens = await create_tokens(str(user.id))
        refresh_backend.refresh_transport.set_cookies(
            response, tokens[settings.COOKIE_NAME]
        )

        return {"access_token": tokens["access_token"], "token_type": "bearer"}

    @router.post(
        "/logout",
        responses=logout_responses,
    )
    async def logout(
        request: Request,
        response: Response,
        user=Depends(authenticator.current_user()),
        redis_client=Depends(get_redis_client),
    ):
        refresh_token = (
            await refresh_backend.refresh_transport.get_refresh_token(request)
        )
        if refresh_token:
            await redis_client.revoke_refresh_token(refresh_token)
        refresh_backend.refresh_transport.delete_cookies(response)
        response.delete_cookie(settings.COOKIE_NAME)
        return {"message": "Successfully logged out"}

    return router


users_router.include_router(
    get_auth_router(
        backend=get_auth_backend(),
        user_manager=get_user_manager(),
        authenticator=fastapi_users.authenticator,
        requires_verification=False,
    ),
    prefix="/auth/jwt",
    tags=["auth"],
)
