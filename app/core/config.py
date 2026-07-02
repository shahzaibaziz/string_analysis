from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "String Analysis API"
    APP_DESCRIPTION: str = "Accepts a string and returns basic analysis metrics."
    APP_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/v1"

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True

    MAX_STRING_LENGTH: int = 100
    LOG_LEVEL: str = "INFO"


settings = Settings()
