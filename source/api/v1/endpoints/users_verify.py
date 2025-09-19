from apps.user_manager import get_user_manager
from fastapi import APIRouter, Body, Depends, Request, status
from fastapi_users import BaseUserManager, models, schemas
from fastapi_users.router.common import ErrorCode, ErrorModel
from http_exceptions_handler import HttpExceptionsHandler
from pydantic import EmailStr
from schemas.users_base import UserBaseSchema

verify_router = APIRouter(prefix="/users")


@verify_router.post(
    "/request-verify-token",
    status_code=status.HTTP_202_ACCEPTED,
    name="verify:request-token",
    tags=["verify"],
)
async def request_verify_token(
    request: Request,
    email: EmailStr = Body(..., embed=True),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(
        get_user_manager
    ),
) -> None:
    with HttpExceptionsHandler():
        user = await user_manager.get_by_email(email)
        await user_manager.request_verify(user, request)


VERIFY_RESPONSES = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.VERIFY_USER_BAD_TOKEN: {
                        "summary": "Bad token, not existing user or not the e-mail currently set for the user.",
                        "value": {"detail": ErrorCode.VERIFY_USER_BAD_TOKEN},
                    },
                    ErrorCode.VERIFY_USER_ALREADY_VERIFIED: {
                        "summary": "The user is already verified.",
                        "value": {
                            "detail": ErrorCode.VERIFY_USER_ALREADY_VERIFIED
                        },
                    },
                }
            }
        },
    }
}


@verify_router.post(
    "/verify",
    response_model=UserBaseSchema,
    name="verify:verify",
    tags=["verify"],
    responses=VERIFY_RESPONSES,
)
async def verify(
    request: Request,
    token: str = Body(..., embed=True),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(
        get_user_manager
    ),
):
    with HttpExceptionsHandler():
        user = await user_manager.verify(token, request)
        return schemas.model_validate(UserBaseSchema, user)
