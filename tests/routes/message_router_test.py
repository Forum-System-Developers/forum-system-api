from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from forum_system_api.main import app
from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.user import User
from forum_system_api.schemas.message import MessageCreate, MessageResponse
from forum_system_api.services.auth_service import get_current_user
from forum_system_api.services.websocket_manager import WebSocketManager
from tests.services import test_data as td


MESSAGE_ENDPOINT_SEND_MESSAGE = "/api/v1/messages/"
MESSAGE_CREATE_BY_USERNAME = "/api/v1/messages/by-username"


client = TestClient(app)


class MessageRouterTests(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.mock_db = MagicMock(spec=Session)
        self.user = User(**td.USER_1)
        self.message_response = MessageResponse(**td.MESSAGE_1)
        self.receiver_id = UUID(td.MESSAGE_CREATE['receiver_id'])

    def tearDown(self) -> None:
        app.dependency_overrides = {}
    
    @patch.object(WebSocketManager, 'send_message_as_json', new_callable=AsyncMock)
    @patch('forum_system_api.api.api_v1.routes.message_router.send_message')
    async def test_create_message_returns201_onSuccess(self, mock_send_message, mock_ws_send_message_as_json):
        # Arrange
        mock_send_message.return_value = td.MESSAGE_1
        app.dependency_overrides[get_current_user] = lambda: self.user
        app.dependency_overrides[get_db] = lambda: self.mock_db

        # Act
        response = client.post(MESSAGE_ENDPOINT_SEND_MESSAGE, json=td.MESSAGE_CREATE)

        # Assert
        mock_send_message.assert_called_once_with(
            db=self.mock_db, 
            message_data=MessageCreate(**td.MESSAGE_CREATE), 
            user=self.user
        )
        mock_ws_send_message_as_json.assert_awaited_once_with(
            message=self.message_response, 
            receiver_id=self.receiver_id
        )
        self.assertEqual(response.status_code, 201)

    @patch.object(WebSocketManager, 'send_message_as_json', new_callable=AsyncMock)
    @patch('forum_system_api.api.api_v1.routes.message_router.send_message')
    @patch('forum_system_api.api.api_v1.routes.message_router.user_service.get_by_username')
    async def test_createMessageByUsername_returns201_onSuccess(
        self, 
        mock_get_by_username, 
        mock_send_message, 
        mock_ws_send_message_as_json
    ) -> None:
        # Arrange
        mock_get_by_username.return_value = self.user
        mock_send_message.return_value = td.MESSAGE_1
        app.dependency_overrides[get_current_user] = lambda: self.user
        app.dependency_overrides[get_db] = lambda: self.mock_db

        # Act
        response = client.post(MESSAGE_CREATE_BY_USERNAME, json=td.MESSAGE_CREATE_BY_USERNAME)

        # Assert
        mock_send_message.assert_called_once_with(
            db=self.mock_db, 
            message_data=MessageCreate(**td.MESSAGE_CREATE), 
            user=self.user
        )
        mock_ws_send_message_as_json.assert_awaited_once_with(
            message=self.message_response, 
            receiver_id=self.user.id
        )
        self.assertEqual(response.status_code, 201)


    @patch('forum_system_api.api.api_v1.routes.message_router.user_service.get_by_username')
    async def test_createMessageByUsername_returns400_whenRecipientNotFound(self, mock_get_by_username):
        # Arrange
        mock_get_by_username.return_value = None
        app.dependency_overrides[get_current_user] = lambda: self.user
        app.dependency_overrides[get_db] = lambda: self.mock_db

        # Act
        response = client.post(MESSAGE_CREATE_BY_USERNAME, json=td.MESSAGE_CREATE_BY_USERNAME)

        # Assert
        self.assertEqual(response.status_code, 400)
