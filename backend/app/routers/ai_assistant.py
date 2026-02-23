from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.preference import ChatMessage, ChatResponse
from app.services.ai_assistant import get_ai_response
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/ai-assistant", tags=["AI Assistant"])


@router.post("/chat", response_model=ChatResponse)
def chat(data: ChatMessage, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = get_ai_response(db, current_user.id, data.message, data.conversation_history or [])
    return ChatResponse(response=result["response"], restaurants=result["restaurants"])
