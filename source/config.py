from pydantic import Field, model_validator
from pydantic_settings import BaseSettings


class BasicSettings(BaseSettings):

    PROJECT_NAME: str = Field(default='PROJECT_NAME')
    ENVIRONMENT: str = Field(default='ENVIRONMENT')
    LOG_DIR: str = Field(default='LOG_DIR')


class TestSettings(BasicSettings):

    HOST: str = Field(default='HOST')
    V1: str = Field(default='V1')
    HTTP_SECURE: str = Field(default='HTTP_SECURE')
    HTTP_PORT: int = Field(default=80)


class ProdSettings(BasicSettings):

    HOST: str = Field(default='HOST')
    V1: str = Field(default='V1')
    HTTP_SECURE: str = Field(default='HTTP_SECURE')
    HTTP_PORT: int = Field(default=80)

    DB_HOST: str = Field(default='DB_HOST')
    DB_PASS: str = Field(default='DB_PASS')
    DB_PORT: str = Field(default='DB_PORT')
    DB_USER: str = Field(default='DB_USER')
    DB_NAME: str = Field(default='DB_NAME')
    DB_URL: str = Field(default='DB_URL')

    VERIFY_TOKEN_SECRET: str = Field(default='VERIFY_TOKEN_SECRET')
    SENDER_EMAIL: str = Field(default='SENDER_EMAIL')
    SENDER_PASSWORD: str = Field(default='SENDER_PASSWORD')
    SMTP_PORT: int = Field(default=465)
    SMTP_SERVER: str = Field(default='SMTP_SERVER')

    JWT_SECRET: str = Field(default='JWT_SECRET')

    @model_validator(mode='before')
    def get_database_url(cls, values):

        values['DB_URL'] = (
            f"postgresql+asyncpg://{values['DB_USER']}:{values['DB_PASS']}"
            + f"@{values['DB_HOST']}:{values['DB_PORT']}/{values['DB_NAME']}"
        )
        return values


# base_settings = BasicSettings()
# if base_settings.ENVIRONMENT == 'test':
#     settings = TestSettings()
# elif base_settings.ENVIRONMENT == 'prod':
#     settings = ProdSettings()
# elif base_settings.ENVIRONMENT == 'local':
#     settings = ProdSettings()
# else:
#     settings = TestSettings()

settings = ProdSettings()
