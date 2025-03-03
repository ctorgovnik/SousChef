from .db_manager import DatabaseManager
from .web_search import WebSearchLLM
from .llms.chat_llm import ChatLLM
from .llms.web_llm import WebLLM
from typing import Dict, Any

class LLMManager:
    def __init__(self, config: Dict[str, Any]):
        self.db_manager = DatabaseManager()
        self.web_search_llm = WebSearchLLM()
        self.chat_llm = ChatLLM()
        self.web_llm = WebLLM()
        self.initialize_llms(config)
    
    async def initialize_llms(self, config: Dict[str, Any]):
        await self.chat_llm.initialize(config.get("chat_llm", {}))
        await self.web_llm.initialize(config.get("web_llm", {}))
    
    async def process_user_query(self, query: str) -> str:
        if self._is_recipe_query(query):
            return await self.recipe_llm.generate(query)
        return await self.chat_llm.generate(query)
    
    async def generate_response(self, query: str, context: str) -> str:
        # Implement your main LLM logic here
        pass 

    def _is_recipe_query(self, query: str) -> bool:
        # Implement your logic to determine if a query is a recipe query
        return False  # Placeholder, actual implementation needed

    async def process_user_query_with_context(self, query: str, context: str) -> str:
        # First check if we have relevant info in DB
        db_context = await self.db_manager.get_relevant_context(query)
        
        if not db_context:
            # If no relevant info in DB, use web search LLM
            web_context = await self.web_search_llm.search(query)
            # Store new information
            await self.db_manager.store_context(query, web_context)
            context = web_context
        else:
            context = db_context
            
        # Generate response using context
        response = await self.generate_response(query, context)
        return response 