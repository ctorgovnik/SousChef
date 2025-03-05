import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock
from main import app, get_settings
from src.core.llm_manager import LLMManager
from src.config.settings import Settings, SettingsConfigDict
from src.api.routes import get_llm_manager

@pytest.fixture
def mock_settings():
    # Override model_config for testing
    Settings.model_config = SettingsConfigDict(
        env_prefix="", 
        env_file="",    
    )
    
    return Settings(
        chat_llm={
            "model": "gpt-4.5",
            "api_key": "test-key",
            "system_prompt": "test assistant"
        },
        web_llm={
            "model": "gpt-4.5",
            "api_key": "test-key",
            "system_prompt": "test web assistant"
        }
    )

@pytest.fixture
def mock_llm_manager():
    manager = Mock(spec=LLMManager)
    manager.process_user_query = AsyncMock(return_value="mocked response")
    return manager

@pytest.fixture
def client(mock_llm_manager, mock_settings):
    # Setup
    app.dependency_overrides[get_llm_manager] = lambda: mock_llm_manager
    app.dependency_overrides[get_settings] = lambda: mock_settings
    client = TestClient(app)
    
    yield client 
    
    # Cleanup after test
    app.dependency_overrides.clear()


def test_valid_chat_request(client, mock_llm_manager):
    response = client.post("/api/v1/chat", json={"request": {"prompt": "test prompt"}}) 
    
    assert response.status_code == 200
    assert response.json() == {"response": "mocked response"}
    mock_llm_manager.process_user_query.assert_called_once_with("test prompt")
    
