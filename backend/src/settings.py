from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    google_gen_ai_api_key: str
    google_gen_ai_model_name: str
    google_gen_ai_model_temp: float
    google_gen_ai_model_max_tokens: int
    google_gen_ai_model_top_p: float
    google_gen_ai_model_prompt_path: str

    data_directory_path: Path
