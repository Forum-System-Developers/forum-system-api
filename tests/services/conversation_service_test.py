import unittest
from unittest.mock import MagicMock, patch
from uuid import uuid4

from fastapi import HTTPException

from forum_system_api.services.conversation_service import (
    get_conversation,
    get_messages_in_conversation,
    get_conversations_for_user,
    get_messages_with_receiver,
    get_users_from_conversations,
)
from forum_system_api.persistence.models.user import User
from forum_system_api.persistence.models.message import Message
from forum_system_api.persistence.models.conversation import Conversation
from tests.services.test_data import USER_1, USER_2
from tests.services.utils import assert_filter_called_with

class TestConversationService(unittest.TestCase):

    def setUp(self) -> None:
        self.db = MagicMock()
        self.user = User(**USER_1)
        self.user_2= User(**USER_2)
        self.conversation_id = uuid4()
        self.conversation = Conversation(id=self.conversation_id, user1_id=self.user.id, user2_id=uuid4())
        self.message1 = Message(id=uuid4(), conversation_id=self.conversation_id, content="Hello")
        self.message2 = Message(id=uuid4(), conversation_id=self.conversation_id, content="World")

    def test_get_conversation_found(self) -> None:
        # Arrange
        self.db.query.return_value.filter.return_value.first.return_value = self.conversation

        # Act
        conversation = get_conversation(self.db, self.conversation_id)

        # Assert
        self.assertEqual(conversation.id, self.conversation_id)
        assert_filter_called_with(self.db.query.return_value, Conversation.id == self.conversation_id)

    def test_get_conversation_not_found(self) -> None:
        # Arrange
        self.db.query.return_value.filter.return_value.first.return_value = None

        # Act and Assert
        with self.assertRaises(HTTPException) as context:
            get_conversation(self.db, self.conversation_id)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "Conversation not found")
        assert_filter_called_with(self.db.query.return_value, Conversation.id == self.conversation_id)

    @patch('forum_system_api.services.conversation_service.get_conversation')
    def test_get_messages_in_conversation_found(self, mock_get_conversation) -> None:
        # Arrange
        mock_get_conversation.return_value = self.conversation
        self.db.query.return_value.filter.return_value.all.return_value = [self.message1, self.message2]

        # Act
        messages = get_messages_in_conversation(self.db, self.conversation_id)

        # Assert
        self.assertEqual(len(messages), 2)
        assert_filter_called_with(self.db.query.return_value, Message.conversation_id == self.conversation_id)

    @patch('forum_system_api.services.conversation_service.get_conversation')
    def test_get_messages_in_conversation_not_found(self, mock_get_conversation) -> None:
        # Arrange
        mock_get_conversation.side_effect = HTTPException(status_code=404, detail="Conversation not found")

        # Act and Assert
        with self.assertRaises(HTTPException) as context:
            get_messages_in_conversation(self.db, self.conversation_id)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "Conversation not found")

    def test_get_conversations_for_user(self) -> None:
        # Arrange
        self.db.query.return_value.filter.return_value.all.return_value = [self.conversation]

        # Act
        conversations = get_conversations_for_user(self.db, self.user)

        # Assert
        self.assertEqual(len(conversations), 1)
        self.assertEqual(conversations[0].id, self.conversation.id)
        expected_filter = (Conversation.user1_id == self.user.id) | (Conversation.user2_id == self.user.id)
        assert_filter_called_with(self.db.query.return_value, expected_filter)

    @patch('forum_system_api.services.conversation_service.get_conversations_for_user')
    def test_get_users_from_conversations_found(self, mock_get_conversations_for_user) -> None:
        # Arrange
        conversation1 = Conversation(id=self.conversation_id, user1_id=self.user.id, user2_id=uuid4())
        conversation2 = Conversation(id=uuid4(), user1_id=uuid4(), user2_id=self.user.id)

        mock_get_conversations_for_user.return_value = [conversation1, conversation2]

        user1 = self.user
        user2 = self.user_2
        self.db.query.return_value.filter.return_value.all.return_value = [user1, user2]

        # Act
        users = get_users_from_conversations(self.db, self.user)

        # Assert
        self.assertEqual(len(users), 2)
        self.assertIn(user1, users)
        self.assertIn(user2, users)

        expected_filter = User.id.in_({conversation1.user2_id, conversation2.user1_id})
        assert_filter_called_with(self.db.query.return_value, expected_filter)

    @patch('forum_system_api.services.conversation_service.get_conversations_for_user')
    def test_get_users_from_conversations_not_found(self, mock_get_conversations_for_user) -> None:
        # Arrange
        mock_get_conversations_for_user.return_value = [self.conversation]
        self.db.query.return_value.filter.return_value.all.return_value = []

        # Act and Assert
        with self.assertRaises(HTTPException) as context:
            get_users_from_conversations(self.db, self.user)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "No users found with exchanged messages")
        expected_filter = User.id.in_({self.conversation.user2_id})
        assert_filter_called_with(self.db.query.return_value, expected_filter)

    def test_get_messages_with_receiver_conversation_found(self) -> None:
        # Arrange
        self.db.query.return_value.filter.return_value.first.return_value = self.conversation
        self.db.query.return_value.filter.return_value.all.return_value = [self.message1, self.message2]

        # Act
        messages = get_messages_with_receiver(self.db, self.user.id, self.user_2.id)

        # Assert
        self.assertEqual(len(messages), 2)

    def test_get_messages_with_receiver_conversation_not_found(self) -> None:
        # Arrange
        self.db.query.return_value.filter.return_value.first.return_value = None

        # Act and Assert
        with self.assertRaises(HTTPException) as context:
            get_messages_with_receiver(self.db, self.user.id, self.user_2.id)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "Conversation not found")

    def test_get_messages_with_receiver_no_messages_found(self) -> None:
        # Arrange
        self.db.query.return_value.filter.return_value.first.return_value = self.conversation
        self.db.query.return_value.filter.return_value.all.return_value = []

        # Act and Assert
        with self.assertRaises(HTTPException) as context:
            get_messages_with_receiver(self.db, self.user.id, self.user_2.id)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "No messages found in this conversation")