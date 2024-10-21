import unittest
from unittest.mock import MagicMock, patch

from fastapi import HTTPException
from sqlalchemy.orm import Session

from forum_system_api.services.message_service import get_or_create_conversation, send_message
from forum_system_api.persistence.models.user import User
from forum_system_api.persistence.models.conversation import Conversation
from forum_system_api.schemas.message import MessageCreate
from tests.services.test_data import USER_1, USER_2
from tests.services.utils import assert_filter_called_with


class MessageService_Should(unittest.TestCase):

    def setUp(self):
        self.mock_db = MagicMock(spec=Session)
        
        self.sender = User(**USER_1)
        self.receiver = User(**USER_2)
        self.conversation = Conversation(id=1, user1_id=self.sender.id, user2_id=self.receiver.id)
        self.message_data = MessageCreate(content="Hello!", receiver_id=self.receiver.id)

    def test_get_or_create_conversation_existing_conversation(self):
        # Arrange
        self.mock_db.query.return_value.filter.return_value.first.return_value = self.conversation

        # Act
        result = get_or_create_conversation(self.mock_db, self.sender.id, self.receiver.id)

        # Assert
        self.assertEqual(result, self.conversation)
        assert_filter_called_with(
            self.mock_db.query.return_value,
            ((Conversation.user1_id == self.sender.id) & (Conversation.user2_id == self.receiver.id)) |
            ((Conversation.user1_id == self.receiver.id) & (Conversation.user2_id == self.sender.id))
        )

    def test_get_or_create_conversation_creates_new_conversation(self):
        # Arrange
        self.mock_db.query.return_value.filter.return_value.first.return_value = None
        self.mock_db.add.return_value = None

        # Act
        result = get_or_create_conversation(self.mock_db, self.sender.id, self.receiver.id)

        # Assert
        self.mock_db.add.assert_called_once_with(result)
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once_with(result)
        self.assertEqual(result.user1_id, self.sender.id)
        self.assertEqual(result.user2_id, self.receiver.id)
