import unittest
from unittest.mock import MagicMock, patch
from uuid import uuid4

from fastapi import HTTPException

from forum_system_api.services.conversation_service import (
    get_conversation,
    get_messages_in_conversation,
    get_conversations_for_user,
    get_users_from_conversations,
)
from forum_system_api.persistence.models.user import User
from forum_system_api.persistence.models.message import Message
from forum_system_api.persistence.models.conversation import Conversation
from tests.services.test_data import USER_1
from tests.services.utils import assert_filter_called_with

class TestConversationService(unittest.TestCase):

    def setUp(self) -> None:
        self.db = MagicMock()
        self.user = User(**USER_1)
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
