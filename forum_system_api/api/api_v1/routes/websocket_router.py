from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from forum_system_api.persistence.database import get_db
from forum_system_api.services import auth_service
from forum_system_api.services.websocket_manager import websocket_manager


websocket_router = APIRouter(prefix='/ws')


@websocket_router.websocket('/connect')
async def websocket_connect(
    websocket: WebSocket,
    db: Session = Depends(get_db)
) -> None:
    await websocket.accept()
    user_id = None
    try:
        data = await websocket.receive_json()
        user_id = auth_service.authenticate_websocket_user(data=data, db=db)
        
        if user_id is None:
            await websocket.close()
            return
        
        await websocket_manager.connect(websocket=websocket, user_id=user_id)
    
        while True:
            await websocket.receive_text()
    except (WebSocketDisconnect, RuntimeError):
        await websocket_manager.disconnect(user_id)
    finally:
        await websocket_manager.close_connection(websocket)
