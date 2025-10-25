from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    google_gen_ai_api_key: str
    google_gen_ai_model_name: str
    google_gen_ai_model_temp: float
    google_gen_ai_model_max_tokens: int
    google_gen_ai_model_top_p: float
    google_gen_ai_model_prompt_path: Path

    local_storage_dir_path: Path

    @computed_field
    @property
    def google_gen_ai_model_instructions(self) -> str:
        return self.google_gen_ai_model_prompt_path.read_text(encoding="utf-8")
