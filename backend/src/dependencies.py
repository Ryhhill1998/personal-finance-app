from typing import Annotated

from src.model_service import ModelService
from src.settings import Settings


def get_settings() -> Settings:
    return Settings()


def get_model_service(settings: Annotated[Settings, get_settings]) -> ModelService:
    return ModelService(
        api_key=settings.google_gen_ai_api_key,
        model_name=settings.google_gen_ai_model_name,
        temperature=settings.google_gen_ai_model_temp,
        max_tokens=settings.google_gen_ai_model_max_tokens,
        top_p=settings.google_gen_ai_model_top_p,
        instructions=settings.google_gen_ai_model_instructions,
    )
