from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....persistence.database import get_db
from ....persistence.models.user import User
from ....schemas.message import MessageCreate, MessageResponse
from ....services.message_service import send_message
from forum_system_api.services.auth_service import get_current_user


message_router = APIRouter(prefix="/messages", tags=["messages"])

@message_router.post("/", response_model=MessageResponse)
def create_message(message_data: MessageCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> MessageResponse:
    recipient = db.query(User).filter(User.id == message_data.receiver_id).first()
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")

    return send_message(db, message_data, user)
