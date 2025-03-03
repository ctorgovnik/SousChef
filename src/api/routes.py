from fastapi import APIRouter, HTTPException
from ..core.llm_manager import LLMManager
from ..models.schemas import ChatRequest

router = APIRouter()
llm_manager = LLMManager()

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        response = await llm_manager.process_user_query(request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 