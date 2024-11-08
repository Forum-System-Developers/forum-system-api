import unittest
from unittest.mock import AsyncMock, patch

from fastapi import WebSocket
from fastapi.websockets import WebSocketState

from forum_system_api.services.websocket_manager import WebSocketManager
from forum_system_api.schemas.message import MessageResponse
from tests.services.test_data import MESSAGE_1, VALID_USER_ID


class WebSocketManager_Should(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.manager = WebSocketManager()
        self.user_id = VALID_USER_ID
        self.websocket = AsyncMock(spec=WebSocket)
        self.message = MessageResponse(**MESSAGE_1)

    async def test_connect_addsNewConnection(self) -> None:
        # Act
        await self.manager.connect(self.websocket, self.user_id)

        # Assert
        self.assertIn(self.user_id, self.manager._active_connections)
        self.assertEqual(self.manager._active_connections[self.user_id], self.websocket)


    @patch.object(WebSocketManager, 'disconnect', new_callable=AsyncMock) 
    async def test_connect_replacesExistingConnection(self, mock_disconnect) -> None:
        # Arrange
        previous_websocket = AsyncMock(spec=WebSocket)
        self.manager._active_connections[self.user_id] = previous_websocket

        # Act
        await self.manager.connect(self.websocket, self.user_id)

        # Assert
        mock_disconnect.assert_awaited_once_with(self.user_id)
        self.assertEqual(self.websocket, self.manager._active_connections[self.user_id])

    @patch.object(WebSocketManager, 'close_connection', new_callable=AsyncMock)
    async def test_disconnect_removesConnection(self, mock_close_connection) -> None:
        # Arrange
        self.manager._active_connections[self.user_id] = self.websocket

        # Act
        await self.manager.disconnect(self.user_id)

        # Assert
        self.assertNotIn(self.user_id, self.manager._active_connections)
        mock_close_connection.assert_awaited_once_with(self.websocket)

    async def test_disconnect_doesNothingIfNoConnection(self) -> None:
        # Act
        await self.manager.disconnect(self.user_id)

        # Assert
        self.websocket.close.assert_not_awaited()

    async def test_closeConnection_closesConnectedWebSocket(self) -> None:
        # Arrange
        self.websocket.application_state = WebSocketState.CONNECTED
        # self.websocket.close = AsyncMock()

        # Act
        await self.manager.close_connection(self.websocket)

        # Assert
        self.websocket.close.assert_awaited_once()

    async def test_closeConnection_doesNothingIfNotConnected(self) -> None:
        # Arrange
        self.websocket.application_state = WebSocketState.DISCONNECTED

        # Act
        await self.manager.close_connection(self.websocket)

        # Assert
        self.websocket.close.assert_not_awaited()

    async def test_sendMessageAsJson_sendsMessage(self) -> None:
        # Arrange
        self.manager._active_connections[self.user_id] = self.websocket
        self.websocket.application_state = WebSocketState.CONNECTED

        # Act
        await self.manager.send_message_as_json(self.message, self.user_id)

        # Assert
        self.websocket.send_text.assert_awaited_once_with(self.message.model_dump_json())

    async def test_sendMessage_sendsMessage(self) -> None:
        # Arrange
        self.manager._active_connections[self.user_id] = self.websocket
        self.websocket.application_state = WebSocketState.CONNECTED
        message = 'Test message'

        # Act
        await self.manager.send_message(message, self.user_id)

        # Assert
        self.websocket.send_text.assert_awaited_once_with(message)

    async def test_sendMessage_doesNothingIfNotConnected(self) -> None:
        # Arrange
        self.manager._active_connections[self.user_id] = self.websocket
        self.websocket.application_state = WebSocketState.DISCONNECTED
        message = 'Test message'

        # Act
        await self.manager.send_message(message, self.user_id)

        # Assert
        self.websocket.send_text.assert_not_awaited()
