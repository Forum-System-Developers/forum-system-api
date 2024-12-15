from uuid import UUID

from fastapi import APIRouter, Depends, Path

from forum_system_api.persistence.models.user import User
from forum_system_api.schemas.message import MessageResponse
from forum_system_api.schemas.user import UserResponse
from forum_system_api.services.auth_service import get_current_user
from forum_system_api.services.conversation_service import (
    get_messages_with_receiver,
    get_users_from_conversations,
)

conversation_router = APIRouter(prefix="/conversations", tags=["conversations"])


@conversation_router.get(
    "/contacts",
    response_model=list[UserResponse],
    description="Get all users who have had conversations with the current user",
)
def get_users_with_conversations_route(
    user: User = Depends(get_current_user),
) -> list[UserResponse]:
    users = get_users_from_conversations(user)
    return [UserResponse.model_validate(user, from_attributes=True) for user in users]


@conversation_router.get(
    "/{receiver_id}",
    response_model=list[MessageResponse],
    description="Get all messages between the current user and the specified user",
)
def get_messages_with_receiver_route(
    receiver_id: UUID = Path(
        ..., description="The ID of the user to get messages with"
    ),
    user: User = Depends(get_current_user),
) -> list[MessageResponse]:
    return [
        MessageResponse.model_validate(message, from_attributes=True)
        for message in get_messages_with_receiver(user, receiver_id)
    ]
