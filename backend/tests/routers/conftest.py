from pathlib import Path
from typing import Generator, Any

import pytest

from src.dependencies import get_settings
from src.main import app
from src.settings import Settings


@pytest.fixture
def override_get_settings(tmp_path: Path) -> Generator[None, Any, None]:
    test_settings = Settings(
        google_gen_ai_api_key="",
        google_gen_ai_model_name="",
        google_gen_ai_model_temp=1,
        google_gen_ai_model_max_tokens=8000,
        google_gen_ai_model_top_p=0.95,
        google_gen_ai_model_prompt_path=Path("src/prompt.txt"),
        local_storage_dir_path=tmp_path,
    )
    app.dependency_overrides[get_settings] = lambda: test_settings
    yield

    app.dependency_overrides = {}
