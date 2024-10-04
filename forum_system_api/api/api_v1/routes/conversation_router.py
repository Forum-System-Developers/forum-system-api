from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ....persistence.database import get_db
from ....schemas.message import MessageResponse
from ....schemas.user import UserResponse
from ....services.conversation_service import get_messages_by_conversation, get_users_with_conversations


conversation_router = APIRouter(prefix="/conversations", tags=["conversations"])


@conversation_router.get("/{conversation_id}", response_model=list[MessageResponse])
def read_messages_in_conversation(conversation_id: UUID, db: Session = Depends(get_db)):
    return get_messages_by_conversation(db, conversation_id)

@conversation_router.get("/{user_id}/contacts", response_model=list[UserResponse])
def get_users_with_conversations_route(user_id: UUID, db: Session = Depends(get_db)) -> list[UserResponse]:
    return get_users_with_conversations(db, user_id)
