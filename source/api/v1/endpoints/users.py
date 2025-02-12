
from apps.users import auth_backend, fastapi_users
from fastapi import APIRouter
from schemas.users_base import UserBaseSchema

users_router = APIRouter(prefix='/users')

users_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth']
)

users_router.include_router(
    fastapi_users.get_register_router(
        user_schema=UserBaseSchema,
        user_create_schema=UserBaseSchema),
    prefix='/auth',
    tags=['auth'],
)

users_router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix='/auth',
    tags=['auth'],
)

users_router.include_router(
    fastapi_users.get_users_router(
        user_schema=UserBaseSchema,
        user_update_schema=UserBaseSchema),
    tags=['users'],
)


# @router_users.get('/authenticated-route')
# async def authenticated_route(user: User = Depends(current_active_user)):
#     return {'message': f'Hello {user.email}!'}
