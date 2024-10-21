from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from forum_system_api.schemas.message import MessageResponse
from forum_system_api.schemas.user import UserResponse
from forum_system_api.persistence.models.user import User
from forum_system_api.persistence.models.message import Message
from forum_system_api.persistence.models.conversation import Conversation


def get_conversation(db: Session, conversation_id: UUID) -> Conversation:
    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404, detail="Conversation not found"
        )

    return conversation


def get_messages_in_conversation(db: Session, conversation_id: UUID) -> list[MessageResponse]:
    get_conversation(db, conversation_id)

    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .all()
    )

    return [message for message in messages]


def get_conversations_for_user(db: Session, user: User) -> list[Conversation]:
    conversations = (
        db.query(Conversation)
        .filter((Conversation.user1_id == user.id) | (Conversation.user2_id == user.id))
        .all()
    )

    return conversations


def get_users_from_conversations(db: Session, user: User) -> list[UserResponse]:
    conversations = get_conversations_for_user(db, user)

    user_ids = set()
    for conversation in conversations:
        if conversation.user1_id != user.id:
            user_ids.add(conversation.user1_id)
        if conversation.user2_id != user.id:
            user_ids.add(conversation.user2_id)

    users = db.query(User).filter(User.id.in_(user_ids)).all()

    if not users:
        raise HTTPException(
            status_code=404, detail="No users found with exchanged messages"
        )

    return [user for user in users]
