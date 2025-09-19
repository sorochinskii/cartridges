from fastapi_users import exceptions as fast_users_exceptions
from fastapi_users.exceptions import UserNotExists
from http_exceptions import (
    HTTPObjectNotExist,
    HTTPUniqueException,
    HTTPUserAlreadyVerified,
    HTTPUserNotExists,
    HTTPVerifyBadToken,
)
from loguru import logger
from sa_exceptions_handler import ItemNotFound, ItemNotUnique


class HttpExceptionsHandler:
    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_instance, traceback):
        match ex_instance:
            case ItemNotUnique():
                raise HTTPUniqueException
            case ItemNotFound():
                raise HTTPObjectNotExist
            case UserNotExists():
                raise HTTPUserNotExists
            case fast_users_exceptions.InvalidVerifyToken():
                raise HTTPVerifyBadToken
            case fast_users_exceptions.UserAlreadyVerified():
                raise HTTPUserAlreadyVerified
        if ex_instance:
            logger.error(ex_instance)
            raise ex_instance
