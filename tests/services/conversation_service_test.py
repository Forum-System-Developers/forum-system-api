import unittest
from unittest.mock import Mock
from uuid import uuid4

from forum_system_api.persistence.models.message import Message
from forum_system_api.persistence.models.user import User
from forum_system_api.services.conversation_service import (
    get_messages_with_receiver,
    get_users_from_conversations,
)


class GetUsersFromConversations_Should(unittest.TestCase):
    def setUp(self):
        self.user1 = Mock(spec=User)
        self.user2 = Mock(spec=User)
        self.user3 = Mock(spec=User)
        self.receiver_id = uuid4()

        self.conversation = Mock()
        self.conversation.user1 = self.user1
        self.conversation.user2 = self.user2
        self.conversation.messages = [Mock(spec=Message)]

        self.user1.conversations = [self.conversation]

    def test_return_users_in_conversations(self):
        # Act
        users = get_users_from_conversations(self.user1)

        # Assert
        expected_users = {self.user1, self.user2}
        self.assertEqual(set(users), expected_users)

    def test_return_empty_list_if_no_conversations(self):
        # Arrange
        self.user1.conversations = []

        # Act
        users = get_users_from_conversations(self.user1)

        # Assert
        self.assertEqual(set(users), set())

    def test_return_messages_with_receiver(self):
        # Arrange
        self.conversation.user1_id = self.user1.id
        self.conversation.user2_id = self.receiver_id

        self.conversation.messages = [Mock(spec=Message)]

        # Act
        messages = get_messages_with_receiver(self.user1, self.receiver_id)

        # Assert
        self.assertEqual(messages, self.conversation.messages)

    def test_return_empty_list_if_no_conversation_with_receiver(self):
        # Arrange
        self.user1.conversations = []

        # Act
        messages = get_messages_with_receiver(self.user1, self.receiver_id)

        # Assert
        self.assertEqual(messages, [])
