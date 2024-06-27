from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GOOGLE_AUTH_ID: str
    GOOGLE_AUTH_KEY: str
    model_config = SettingsConfigDict(env_file=".env")


envs = Settings()  # type: ignore