from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, Optional

class BaseLLMConfig(BaseSettings):
    model: str
    api_key: str
    temperature: float = 0.7
    max_tokens: int = 1000
    system_prompt: str

class WebSearchConfig(BaseSettings):
    search_engine: str | None = None
    search_api_key: str | None = None

class WebLLM(BaseLLMConfig):
    search_config: WebSearchConfig | None = None

class ChatLLM(BaseLLMConfig):
    pass

class Settings(BaseSettings):
    chat_llm: ChatLLM
    web_llm: WebLLM
    database_url: str | None = None
    api_version: str = "v1"
    
    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        env_nested_delimiter="__"
    ) 