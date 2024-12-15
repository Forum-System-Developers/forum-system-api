from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.user import User
from forum_system_api.schemas.message import (
    MessageCreate,
    MessageCreateByUsername,
    MessageResponse,
)
from forum_system_api.services import user_service
from forum_system_api.services.auth_service import get_current_user
from forum_system_api.services.message_service import send_message
from forum_system_api.services.websocket_manager import websocket_manager

message_router = APIRouter(prefix="/messages", tags=["messages"])


@message_router.post(
    "/", response_model=MessageResponse, status_code=201, description="Send a message"
)
async def create_message(
    message_data: MessageCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MessageResponse:
    message = send_message(db=db, message_data=message_data, user=user)
    await websocket_manager.send_message_as_json(
        message=MessageResponse.model_validate(message),
        receiver_id=message_data.receiver_id,
    )

    return MessageResponse.model_validate(message, from_attributes=True)


@message_router.post(
    "/by-username",
    response_model=MessageResponse,
    status_code=201,
    description="Send a message by username",
)
async def create_message_by_username(
    message_data: MessageCreateByUsername,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MessageResponse:
    receiver = user_service.get_by_username(
        username=message_data.receiver_username, db=db
    )
    if not receiver:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Recipient not found"
        )

    message_create = MessageCreate(
        receiver_id=receiver.id, content=message_data.content
    )

    message = send_message(db=db, message_data=message_create, user=user)
    await websocket_manager.send_message_as_json(
        message=MessageResponse.model_validate(message), receiver_id=receiver.id
    )

    return MessageResponse.model_validate(message, from_attributes=True)
