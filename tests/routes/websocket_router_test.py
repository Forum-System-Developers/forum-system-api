from unittest import TestCase
from unittest.mock import AsyncMock, MagicMock, patch, ANY

from fastapi import WebSocketDisconnect
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from forum_system_api.main import app
from forum_system_api.persistence.database import get_db
from forum_system_api.services.websocket_manager import WebSocketManager
from tests.services.test_data import VALID_USER_ID


WEBSOCKET_CONNECT_ENDPOINT = '/api/v1/ws/connect'


class TestWebSocketRouter_Should(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def setUp(self) -> None:
        self.mock_db = MagicMock(spec=Session)
        self.user_id = VALID_USER_ID
        self.token = {'token': 'valid_token'}

    def tearDown(self) -> None:
        app.dependency_overrides = {}

    @patch.object(WebSocketManager, 'connect', new_callable=AsyncMock)
    @patch('forum_system_api.services.auth_service.authenticate_websocket_user')
    async def test_websocketConnect_successfullyConnects(self, mock_authenticate, mock_connect) -> None:
        # Arrange
        mock_authenticate.return_value = self.user_id
        app.dependency_overrides[get_db] = lambda: self.mock_db

        # Act
        with self.client.websocket_connect(WEBSOCKET_CONNECT_ENDPOINT) as websocket:
            websocket.send_json(self.token)
            websocket.close()

        # Assert
        mock_authenticate.assert_called_once_with(data=self.token, db=self.mock_db)
        mock_connect.assert_awaited_once_with(websocket=ANY, user_id=self.user_id)

    @patch.object(WebSocketManager, 'connect', new_callable=AsyncMock)
    @patch('forum_system_api.services.auth_service.authenticate_websocket_user')
    async def test_websocketConnect_closesOnInvalidUser(self, mock_authenticate, mock_connect) -> None:
        # Arrange
        mock_authenticate.return_value = None
        app.dependency_overrides[get_db] = lambda: self.mock_db

        # Act
        with self.client.websocket_connect(WEBSOCKET_CONNECT_ENDPOINT) as websocket:
            websocket.send_json(self.token)

        # Assert
        mock_authenticate.assert_called_once_with(data=self.token, db=self.mock_db)
        mock_connect.assert_not_called()
        websocket.close.assert_awaited_once()

    @patch.object(WebSocketManager, 'close_connection', new_callable=AsyncMock)
    @patch.object(WebSocketManager, 'disconnect', new_callable=AsyncMock)
    @patch.object(WebSocketManager, 'connect', new_callable=AsyncMock)
    @patch('forum_system_api.services.auth_service.authenticate_websocket_user')
    async def test_websocketDisconnect_handlesWebSocketDisconnect(
        self, 
        mock_authenticate, 
        mock_connect, 
        mock_disconnect, 
        mock_close_connection
    ) -> None:
        # Arrange
        mock_connect.side_effect = WebSocketDisconnect
        mock_authenticate.return_value = self.user_id
        app.dependency_overrides[get_db] = lambda: self.mock_db

        # Act
        with self.client.websocket_connect(WEBSOCKET_CONNECT_ENDPOINT) as websocket:
            websocket.send_json(self.token)
        
        # Assert
        mock_authenticate.assert_called_once_with(data=self.token, db=self.mock_db)
        mock_connect.assert_awaited_once_with(websocket=ANY, user_id=self.user_id)
        mock_disconnect.assert_awaited_once_with(self.user_id)
        mock_close_connection.assert_awaited_once_with(ANY)

    @patch.object(WebSocketManager, 'close_connection', new_callable=AsyncMock)
    @patch.object(WebSocketManager, 'disconnect', new_callable=AsyncMock)
    @patch.object(WebSocketManager, 'connect', new_callable=AsyncMock)
    @patch('forum_system_api.services.auth_service.authenticate_websocket_user')
    async def test_websocketDisconnect_handlesRuntimeError(
        self, 
        mock_authenticate, 
        mock_connect, 
        mock_disconnect, 
        mock_close_connection
    ) -> None:
        # Arrange
        mock_connect.side_effect = RuntimeError
        mock_authenticate.return_value = self.user_id
        app.dependency_overrides[get_db] = lambda: self.mock_db

        # Act
        with self.client.websocket_connect(WEBSOCKET_CONNECT_ENDPOINT) as websocket:
            websocket.send_json(self.token)
        
        # Assert
        mock_authenticate.assert_called_once_with(data=self.token, db=self.mock_db)
        mock_connect.assert_awaited_once_with(websocket=ANY, user_id=self.user_id)
        mock_disconnect.assert_awaited_once_with(self.user_id)
        mock_close_connection.assert_awaited_once_with(ANY)
