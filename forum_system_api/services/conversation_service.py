from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from forum_system_api.schemas.message import MessageResponse
from forum_system_api.schemas.user import UserResponse
from forum_system_api.persistence.models.user import User
from forum_system_api.persistence.models.message import Message
from forum_system_api.persistence.models.conversation import Conversation


def get_conversation(db: Session, conversation_id: UUID) -> Conversation:
    """
    Retrieve a conversation by its ID from the database.
    
    Args:
        db (Session): The database session to use for the query.
        conversation_id (UUID): The unique identifier of the conversation to retrieve.
    Returns:
        Conversation: The conversation object if found.
    Raises:
        HTTPException: If the conversation with the given ID is not found, raises a 404 HTTP exception.
    """
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
    """
    Retrieve all messages in a specific conversation.

    Args:
        db (Session): The database session to use for the query.
        conversation_id (UUID): The unique identifier of the conversation.
    Returns:
        list[MessageResponse]: A list of messages in the specified conversation.
    """
    get_conversation(db, conversation_id)

    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .all()
    )

    return [message for message in messages]


def get_conversations_for_user(db: Session, user: User) -> list[Conversation]:
    """
    Retrieve all conversations for a given user.

    Args:
        db (Session): The database session to use for the query.
        user (User): The user for whom to retrieve conversations.
    Returns:
        list[Conversation]: A list of Conversation objects involving the user.
    """
    conversations = (
        db.query(Conversation)
        .filter((Conversation.user1_id == user.id) | (Conversation.user2_id == user.id))
        .all()
    )

    return conversations


def get_users_from_conversations(db: Session, user: User) -> list[UserResponse]:
    """
    Retrieve a list of users who have had conversations with the given user.
    
    Args:
        db (Session): The database session to use for querying.
        user (User): The user for whom to find conversation partners.
    Returns:
        list[UserResponse]: A list of UserResponse objects representing users 
                            who have exchanged messages with the given user.
    Raises:
        HTTPException: If no users are found who have exchanged messages with the given user.
    """
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


def get_messages_with_receiver(db: Session, user_id: UUID, receiver_id: UUID) -> list[MessageResponse]:
    """
    Retrieve all messages in a conversation between the current user and a specified receiver.

    Args:
        db (Session): The database session to use for the query.
        user_id (UUID): The unique identifier of the current user.
        receiver_id (UUID): The unique identifier of the receiver.
    Returns:
        list[MessageResponse]: A list of messages in the conversation between the two users.
    Raises:
        HTTPException: If no conversation is found or no messages are available.
    """
    # Находим беседу между текущим пользователем и получателем
    conversation = db.query(Conversation).filter(
        ((Conversation.user1_id == user_id) & (Conversation.user2_id == receiver_id)) |
        ((Conversation.user1_id == receiver_id) & (Conversation.user2_id == user_id))
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Получаем все сообщения в найденной беседе
    messages = db.query(Message).filter(Message.conversation_id == conversation.id).all()

    if not messages:
        raise HTTPException(status_code=404, detail="No messages found in this conversation")

    return [message for message in messages]
