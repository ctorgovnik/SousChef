from fastapi import APIRouter, HTTPException, Depends
from ..core.llm_manager import LLMManager
from ..models.schemas import ChatRequest
from ..config.settings import Settings

router = APIRouter()

def get_llm_manager(settings: Settings):
    return LLMManager(settings.dict())  # Settings passed to LLMManager

@router.post("/chat")
async def chat_endpoint(request: ChatRequest, llm_manager = Depends(get_llm_manager)):
    try:
        response = await llm_manager.process_user_query(request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 