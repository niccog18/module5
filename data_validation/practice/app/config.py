from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Contact Book API"
    debug: bool = True

    class Config:
        env_file = ".env"

settings = Settings()