import pytest
from src.config.settings import Settings
import os

@pytest.fixture(autouse=True)
def mock_env_vars():
    """set up test environment variables"""
    # Chat LLM settings
    os.environ["APP_CHAT_LLM__MODEL"] = "gpt-4"
    os.environ["APP_CHAT_LLM__API_KEY"] = "test-key-123"
    os.environ["APP_CHAT_LLM__SYSTEM_PROMPT"] = "test-system-prompt"

    # Web LLM settings
    os.environ["APP_WEB_LLM__MODEL"] = "gpt-4"
    os.environ["APP_WEB_LLM__API_KEY"] = "test-web-llm-key-123"
    os.environ["APP_WEB_LLM__SYSTEM_PROMPT"] = "test-web-llm-system-prompt"
    os.environ["APP_WEB_LLM__SEARCH_CONFIG__SEARCH_ENGINE"] = "google"
    os.environ["APP_WEB_LLM__SEARCH_CONFIG__SEARCH_API_KEY"] = "search-key-123"

    yield

    #cleanup
    for key in os.environ:
        if key.startswith("APP_"):
            del os.environ[key]


def test_settings_chat_llm(mock_env_vars):
    settings = Settings()
    
    assert settings.chat_llm.model == "gpt-4"
    assert settings.chat_llm.api_key == "test-key-123"
    assert settings.chat_llm.system_prompt == "test-system-prompt"

def test_settings_web_llm(mock_env_vars):
    settings = Settings()
    
    assert settings.web_llm.model == "gpt-4"
    assert settings.web_llm.api_key == "test-web-llm-key-123"
    assert settings.web_llm.system_prompt == "test-web-llm-system-prompt"

def test_settings_default_values(mock_env_vars):
    settings = Settings()
    
    assert settings.chat_llm.temperature == 0.7
    assert settings.chat_llm.max_tokens == 1000
    assert settings.web_llm.temperature == 0.7
    assert settings.web_llm.max_tokens == 1000
    assert settings.api_version == "v1"  # Test default value