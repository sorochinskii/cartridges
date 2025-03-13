from fastapi import HTTPException, status
from fastapi_users import exceptions as fast_users_exceptions
from fastapi_users.exceptions import UserNotExists
from fastapi_users.router.common import ErrorCode as FastUsersErrorCode
from loguru import logger
from sa_exceptions_handler import ItemNotFound, ItemNotUnique

HTTPObjectNotExist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Item not found."
)

HTTPUniqueAttrException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Unique attribute exists."
)

HTTPUniqueException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Unique item exists."
)

HTTPUserNotExists = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not exists."
)


HTTPVerifyBadToken = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=FastUsersErrorCode.VERIFY_USER_BAD_TOKEN,
)

HTTPUserAlreadyVerified = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=FastUsersErrorCode.VERIFY_USER_ALREADY_VERIFIED,
)
