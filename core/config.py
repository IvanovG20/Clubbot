from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    bot_token: str
    database_url: str
    redis_url: str
    api_base_url: str = "http://api:8000"


settings = Settings()
