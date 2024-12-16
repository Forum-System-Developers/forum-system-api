import logging
from uuid import UUID

from fastapi import WebSocket
from fastapi.websockets import WebSocketState

from forum_system_api.schemas.message import MessageResponse

logger = logging.getLogger(__name__)


class WebSocketManager:
    """
    Manages WebSocket connections for users.

    Methods:
        connect(websocket: WebSocket, user_id: UUID) -> None:
            Adds a new WebSocket connection for a user.

        disconnect(user_id: UUID) -> None:
            Removes the WebSocket connection for a user.

        close_connection(websocket: WebSocket) -> None:
            Closes the WebSocket connection if it is in the WebSocketState.CONNECTED state.

        send_message_as_json(message: MessageResponse, receiver_id: UUID) -> None:
            Sends a MessageResponse object as JSON to a specific user via their WebSocket connection.

        send_message(message: str, receiver_id: UUID) -> None:
            Sends a message to a specific user via their WebSocket connection.
    """

    def __init__(self) -> None:
        self._active_connections: dict[UUID, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: UUID) -> None:
        """
        Establishes a WebSocket connection for a given user.

        If the user is already connected, the existing connection is closed before establishing a new one.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
            user_id (UUID): The unique identifier of the user.
        """
        if user_id in self._active_connections:
            logger.info(
                f"User {user_id} is already connected. Closing existing connection."
            )
            await self.disconnect(user_id)

        self._active_connections[user_id] = websocket
        logger.info(f"User {user_id} connected from {websocket.client}.")

    async def disconnect(self, user_id: UUID) -> None:
        """
        Disconnects a user by their user_id.

        This method removes the user's websocket connection from the active connections
        and closes the websocket connection if it exists.

        Args:
            user_id (UUID): The unique identifier of the user to disconnect.
        """
        websocket = self._active_connections.pop(user_id, None)
        logger.info(f"User {user_id} removed from the active connections.")

        await self.close_connection(websocket)

    async def close_connection(self, websocket: WebSocket | None) -> None:
        """
        Closes the WebSocket connection if it is in the WebSocketState.CONNECTED state.

        Args:
            websocket (WebSocket): The WebSocket connection to be closed.
        """
        if (
            websocket is not None
            and websocket.application_state == WebSocketState.CONNECTED
        ):
            try:
                logger.info(f"Closing WebSocket connection from {websocket.client}.")
                await websocket.close()
            except (RuntimeError, ConnectionError) as e:
                logger.error(
                    f"WebSocket connection from {websocket.client} is already closed. Error: {e}"
                )

    async def send_message_as_json(
        self, message: MessageResponse, receiver_id: UUID
    ) -> None:
        """
        Sends a message to a specified receiver if they are connected.

        Args:
            message (MessageResponse): The message to be sent.
            receiver_id (UUID): The unique identifier of the receiver.
        """
        serialized_message = message.model_dump_json()
        logger.info(
            f"Sending message as json {serialized_message} to user {receiver_id}."
        )

        await self.send_message(message=serialized_message, receiver_id=receiver_id)

    async def send_message(self, message: str, receiver_id: UUID) -> None:
        """
        Sends a message to a specific receiver identified by receiver_id.

        Args:
            message (str): The message to be sent.
            receiver_id (UUID): The unique identifier of the receiver.
        """
        receiver = self._active_connections.get(receiver_id)
        if (
            receiver is not None
            and receiver.application_state == WebSocketState.CONNECTED
        ):
            try:
                logger.info(f"Sending message {message} to user {receiver_id}.")
                await receiver.send_text(message)
            except (RuntimeError, ConnectionError) as e:
                logger.error(
                    f"Failed to send message to user {receiver_id}. Error: {e}"
                )
                await self.disconnect(receiver_id)


websocket_manager = WebSocketManager()
