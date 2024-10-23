import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from forum_system_api.api.api_v1.constants import endpoints as e
from forum_system_api.persistence.database import get_db
from tests.services import test_data as td
from forum_system_api.services.auth_service import get_current_user
from sqlalchemy.orm import Session
from forum_system_api.persistence.models.user import User
from forum_system_api.main import app
from tests.services.test_data_obj import USER_1

client = TestClient(app)

class MessageRouterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_db = MagicMock(spec=Session)
        self.user = User(**USER_1)

    def tearDown(self) -> None:
        app.dependency_overrides = {}

    @patch('forum_system_api.api.api_v1.routes.message_router.send_message')
    def test_create_message_returns201_onSuccess(self, mock_send_message):
        # Arrange
        mock_send_message.return_value = td.MESSAGE_1
        app.dependency_overrides[get_current_user] = lambda: self.user
        app.dependency_overrides[get_db] = lambda: self.mock_db

        # Act
        response = client.post(e.MESSAGE_ENDPOINT_SEND_MESSAGE, json=td.MESSAGE_CREATE)

        # Assert
        self.assertEqual(response.status_code, 201)
