from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Voice Calling Agent"
    app_env: str = "development"
    log_level: str = "INFO"

    llm_provider: str = ""
    llm_api_key: str = ""
    llm_model: str = ""

    stt_provider: str = ""
    tts_provider: str = ""

    frontend_url: str = "http://localhost:4200"

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
