from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.user import User
from forum_system_api.schemas.message import MessageCreate, MessageResponse
from forum_system_api.services.message_service import send_message
from forum_system_api.services.auth_service import get_current_user


message_router = APIRouter(prefix="/messages", tags=["messages"])


@message_router.post("/", response_model=MessageResponse, status_code=201)
def create_message(
    message_data: MessageCreate, 
    user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
) -> MessageResponse:
    return send_message(db, message_data, user)
