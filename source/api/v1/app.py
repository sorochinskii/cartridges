from api.v1.endpoints.buildings import buildings_router
from api.v1.endpoints.rooms import rooms_router
from api.v1.endpoints.users import users_router
from api.v1.endpoints.users_verify import verify_router
from config import settings
from fastapi import FastAPI
from utils import URLBuilder

url_builder = URLBuilder(
    host=settings.HOST,
    protocol=settings.HTTP_SECURE,
    port=settings.HTTP_PORT)
url = url_builder.url()
tags_metadata = [
    {
        'name': 'v1',
        'description': 'API version 1',
        'externalDocs': {
            'description': 'sub-docs',
            'url': url
        }
    },
]

app = FastAPI(openapi_tags=tags_metadata)

app.include_router(rooms_router)
app.include_router(buildings_router)
app.include_router(users_router)
app.include_router(verify_router)
