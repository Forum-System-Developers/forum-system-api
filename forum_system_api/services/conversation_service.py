import logging
from uuid import UUID

from forum_system_api.persistence.models.message import Message
from forum_system_api.persistence.models.user import User

logger = logging.getLogger(__name__)


def get_users_from_conversations(user: User) -> set[User]:
    """
    Retrieve a set of users from the conversations of a given user.

    Args:
        user (User): The user whose conversations are to be analyzed.
    Returns:
        set[User]: A set of users who are participants in the conversations with the given user.
    """
    conversations = user.conversations
    logger.info(f"Retrieved {len(conversations)} conversations for user {user.id}")

    users = set()
    for conversation in conversations:
        if conversation.user1_id != user.id:
            users.add(conversation.user1)
        if conversation.user2_id != user.id:
            users.add(conversation.user2)
    logger.info(f"Retrieved {len(users)} users from conversations")

    return users


def get_messages_with_receiver(user: User, receiver_id: UUID) -> list[Message]:
    """
    Retrieve messages from a conversation between the given user and a receiver.

    Args:
        user (User): The user whose conversations are being queried.
        receiver_id (UUID): The unique identifier of the receiver.
    Returns:
        list[Message]: A list of messages in the conversation with the receiver.
                       Returns an empty list if no conversation exists.
    """
    conversation = next(
        (
            conversation
            for conversation in user.conversations
            if conversation.user1_id == receiver_id
            or conversation.user2_id == receiver_id
        ),
        None,
    )
    logger.info(f"Retrieved conversation between user {user.id} and user {receiver_id}")

    if conversation is None:
        logger.info(
            f"No conversation found between user {user.id} and user {receiver_id}"
        )
        return []

    messages = conversation.messages
    logger.info(f"Retrieved {len(messages)} messages in the conversation")

    return messages
