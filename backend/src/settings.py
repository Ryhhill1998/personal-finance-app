from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    google_gen_ai_api_key: str
    model_name: str
    model_temp: float
    model_max_tokens: int
    model_top_p: float
    model_prompt_path: str
