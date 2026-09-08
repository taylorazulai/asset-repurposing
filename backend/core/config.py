from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    EDENAI_API_KEY: str
    EDENAI_BASE_URL: str = "https://api.edenai.run/v3"
    EDENAI_MODEL: str = "google/gemini-3.8-flash"
    MAX_SOURCE_CHARS: int = 50000
    CORS_ORIGINS: str = "http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
