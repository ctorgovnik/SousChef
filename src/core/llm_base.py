from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseLLM(ABC):
    @abstractmethod
    async def generate(self, prompt: str, context: str = None, **kwargs) -> str:
        """Generate a response from the LLM"""
        pass

    @abstractmethod
    async def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the LLM with configuration"""
        pass 