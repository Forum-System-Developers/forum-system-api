import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from forum_system_api.main import app
from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.user import User
from forum_system_api.services.auth_service import get_current_user
from forum_system_api.api.api_v1.constants import endpoints as e
from tests.services import test_data as td

client = TestClient(app)

class TestConversationRouter_Should(unittest.TestCase):
    
    def setUp(self) -> None:
        self.mock_db = MagicMock(spec=Session)
        self.user = User(**td.USER_1)
    
    def tearDown(self) -> None:
        app.dependency_overrides = {}
    
    @patch('forum_system_api.api.api_v1.routes.conversation_router.get_messages_in_conversation')
    def test_read_messages_in_conversation_returns200_onSuccess(self, mock_get_messages_in_conversation) -> None:
        # Arrange
        mock_get_messages_in_conversation.return_value = [td.MESSAGE_1]
        app.dependency_overrides[get_current_user] = lambda: self.user
        app.dependency_overrides[get_db] = lambda: self.mock_db
        
        # Act
        response = client.get(e.CONVERSATION_MESSAGES_ENDPOINT.format(td.VALID_CONVERSATION_ID))
        
        # Assert
        self.assertEqual(response.status_code, 200)

    @patch('forum_system_api.api.api_v1.routes.conversation_router.get_users_from_conversations')
    def test_get_users_with_conversations_route_returns200_onSuccess(self, mock_get_users_from_conversations) -> None:
        # Arrange
        mock_get_users_from_conversations.return_value = [td.USER_1]
        app.dependency_overrides[get_current_user] = lambda: self.user
        app.dependency_overrides[get_db] = lambda: self.mock_db
        
        # Act
        response = client.get(e.CONVERSATION_CONTACTS_ENDPOINT.format(self.user))
        
        # Assert
        self.assertEqual(response.status_code, 200)