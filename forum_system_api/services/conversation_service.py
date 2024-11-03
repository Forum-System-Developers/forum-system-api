from uuid import UUID

from forum_system_api.persistence.models.user import User
from forum_system_api.persistence.models.message import Message


def get_users_from_conversations(user: User) -> set[User]:
    """
    Retrieve a set of users from the conversations of a given user.

    Args:
        user (User): The user whose conversations are to be analyzed.
    Returns:
        set[User]: A set of users who are participants in the conversations with the given user.
    """
    conversations = user.conversations

    users = set()
    for conversation in conversations:
        if conversation.user1_id != user.id:
            users.add(conversation.user1)
        if conversation.user2_id != user.id:
            users.add(conversation.user2)

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
            if conversation.user1_id == receiver_id or conversation.user2_id == receiver_id
        ),
        None
    )

    if conversation is None:
        return []
    
    return conversation.messages
