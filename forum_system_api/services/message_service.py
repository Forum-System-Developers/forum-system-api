import logging
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from forum_system_api.persistence.models.conversation import Conversation
from forum_system_api.persistence.models.message import Message
from forum_system_api.persistence.models.user import User
from forum_system_api.schemas.message import MessageCreate

logger = logging.getLogger(__name__)


def get_or_create_conversation(
    db: Session, user_id: UUID, receiver_id: UUID
) -> Conversation:
    """
    Retrieve an existing conversation between two users or create a new one if it does not exist.

    Args:
        db (Session): The database session to use for querying and creating the conversation.
        user_id (int): The ID of the first user.
        receiver_id (int): The ID of the second user.
    Returns:
        Conversation: The existing or newly created conversation between the two users.
    """
    conversation = (
        db.query(Conversation)
        .filter(
            (
                (Conversation.user1_id == user_id)
                & (Conversation.user2_id == receiver_id)
            )
            | (
                (Conversation.user1_id == receiver_id)
                & (Conversation.user2_id == user_id)
            )
        )
        .first()
    )

    if not conversation:
        conversation = Conversation(user1_id=user_id, user2_id=receiver_id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        logger.info(f"Created new conversation with ID: {conversation.id}")
    logger.info(f"Conversation ID: {conversation.id}")

    return conversation


def send_message(db: Session, message_data: MessageCreate, user: User) -> Message:
    """
    Sends a message from the given user to the specified receiver.

    Args:
        db (Session): The database session.
        message_data (MessageCreate): The data required to create the message, including receiver ID and content.
        user (User): The user sending the message.
    Returns:
        Message: The created message object.
    Raises:
        HTTPException: If the receiver is not found.
    """
    receiver = db.query(User).filter(User.id == message_data.receiver_id).first()

    if not receiver:
        logger.error(f"Receiver with ID {message_data.receiver_id} not found")
        raise HTTPException(status_code=404, detail="Receiver not found")
    logger.info(f"Receiver found with ID: {receiver.id}")

    conversation = get_or_create_conversation(db, user.id, message_data.receiver_id)
    logger.info(
        f"Getting or creating conversation between user {user.id} and user {message_data.receiver_id}"
    )

    message = Message(
        content=message_data.content, conversation_id=conversation.id, author_id=user.id
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    logger.info(f"Sent message from user {user.id} to user {message_data.receiver_id}")

    return message
