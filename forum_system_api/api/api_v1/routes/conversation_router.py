from uuid import UUID

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.user import User
from forum_system_api.schemas.message import MessageResponse
from forum_system_api.schemas.user import UserResponse
from forum_system_api.services.conversation_service import (
    get_messages_in_conversation,
    get_users_from_conversations,
)
from forum_system_api.services.auth_service import get_current_user


conversation_router = APIRouter(prefix="/conversations", tags=["conversations"])


@conversation_router.get(
        "/{conversation_id}", 
        response_model=list[MessageResponse], 
        description="Read messages in a conversation"
)
def read_messages_in_conversation(
    conversation_id: UUID = Path(..., description="The unique identifier of the conversation"),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[MessageResponse]:
    return get_messages_in_conversation(db, conversation_id)


@conversation_router.get(
        "/{user}/contacts", 
        response_model=list[UserResponse], 
        description="Get all users with whom the current user has conversations"
)
def get_users_with_conversations_route(
    user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
) -> list[UserResponse]:
    return get_users_from_conversations(db, user)
