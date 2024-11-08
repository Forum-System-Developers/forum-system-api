from unittest import TestCase
from unittest.mock import MagicMock, patch, ANY

from fastapi.testclient import TestClient

from forum_system_api.main import app
from forum_system_api.persistence.database import get_db
from forum_system_api.services.websocket_manager import websocket_manager


WEBSOCKET_CONNECT_ENDPOINT = '/api/v1/ws/connect'


class TestWebSocketRouter_Should(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def setUp(self) -> None:
        self.mock_db = MagicMock()
        self.mock_websocket = MagicMock()
        self.mock_user_id = 1

    def tearDown(self) -> None:
        app.dependency_overrides = {}

    @patch('forum_system_api.api.api_v1.routes.websocket_router.websocket_manager.connect')
    @patch('forum_system_api.services.auth_service.authenticate_websocket_user')
    def test_websocketConnect_successfullyConnects(self, mock_authenticate, mock_connect) -> None:
        # Arrange
        mock_authenticate.return_value = self.mock_user_id
        app.dependency_overrides[get_db] = lambda: self.mock_db

        # Act
        with self.client.websocket_connect(WEBSOCKET_CONNECT_ENDPOINT) as websocket:
            websocket.send_json({'token': 'valid_token'})
            websocket.send_text('test_message')
            websocket.close()

        # Assert
        mock_connect.assert_called_once_with(websocket=ANY, user_id=self.mock_user_id)

    @patch('forum_system_api.api.api_v1.routes.websocket_router.websocket_manager.connect')
    @patch('forum_system_api.services.auth_service.authenticate_websocket_user')
    def test_websocketConnect_closesOnInvalidUser(self, mock_authenticate, mock_connect) -> None:
        # Arrange
        mock_authenticate.return_value = None
        app.dependency_overrides[get_db] = lambda: self.mock_db

        # Act
        with self.client.websocket_connect(WEBSOCKET_CONNECT_ENDPOINT) as websocket:
            websocket.send_json({'token': 'invalid_token'})

        # Assert
        mock_connect.assert_not_called()

    @patch('forum_system_api.api.api_v1.routes.websocket_router.websocket_manager.disconnect')
    @patch('forum_system_api.api.api_v1.routes.websocket_router.websocket_manager.connect')
    @patch('forum_system_api.services.auth_service.authenticate_websocket_user')
    def test_websocketDisconnect_handlesDisconnect(self, mock_authenticate, mock_connect, mock_disconnect) -> None:
        # Arrange
        mock_authenticate.return_value = self.mock_user_id
        app.dependency_overrides[get_db] = lambda: self.mock_db

        # Act
        with self.client.websocket_connect(WEBSOCKET_CONNECT_ENDPOINT) as websocket:
            websocket.send_json({'token': 'valid_token'})
            websocket.close()

        # Assert
        mock_connect.assert_called_once_with(websocket=ANY, user_id=self.mock_user_id)
        mock_disconnect.assert_called_once_with(self.mock_user_id)
