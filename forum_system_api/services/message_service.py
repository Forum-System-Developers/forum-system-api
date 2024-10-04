from uuid import UUID

from sqlalchemy.orm import Session

from ..persistence.models.conversation import Conversation
from ..persistence.models.message import Message
from ..schemas.message import MessageCreate


def send_message(db: Session, message_data: MessageCreate, user_id: UUID) -> Message:
    conversation = db.query(Conversation).filter(
        (Conversation.user1_id == user_id) | (Conversation.user2_id == user_id)
    ).first()

    if not conversation:
        conversation = Conversation(user1_id=user_id, user2_id=message_data.receiver_id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    message = Message(content=message_data.content, conversation_id=conversation.id, author_id=user_id)
    db.add(message)
    db.commit()
    db.refresh(message)

    return message
