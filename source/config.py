from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    HOST: str = Field(default='HOST')
    PROJECT_NAME: str = Field(default='PROJECT_NAME')
    LOG_DIR: str = Field(default='LOG_DIR')
    V1: str = Field(default='V1')
    HTTP_SECURE: str = Field(default='HTTP_SECURE')
    HTTP_PORT: int = Field(default=80)
    ENVIRONMENT: str = Field(default='ENVIRONMENT')


settings = Settings()
