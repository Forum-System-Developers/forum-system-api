from fastapi import HTTPException
from sqlalchemy.orm import Session

from forum_system_api.persistence.models.user import User
from forum_system_api.persistence.models.message import Message
from forum_system_api.persistence.models.conversation import Conversation
from forum_system_api.schemas.message import MessageCreate


def send_message(db: Session, message_data: MessageCreate, user: User) -> Message:
    receiver = db.query(User).filter(User.id == message_data.receiver_id).first()

    if not receiver:
        raise HTTPException(status_code=404, detail="receiver not found")

    conversation = db.query(Conversation).filter(
        ((Conversation.user1_id == user.id) & (Conversation.user2_id == message_data.receiver_id)) |
        ((Conversation.user1_id == message_data.receiver_id) & (Conversation.user2_id == user.id))
    ).first()

    if not conversation:
        conversation = Conversation(user1_id=user.id, user2_id=message_data.receiver_id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    message = Message(content=message_data.content, conversation_id=conversation.id, author_id=user.id)
    db.add(message)
    db.commit()
    db.refresh(message)

    return message
