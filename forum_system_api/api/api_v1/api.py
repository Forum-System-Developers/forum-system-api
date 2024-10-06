from fastapi import APIRouter

from .routes.auth_router import auth_router
from .routes.user_router import router as user_router
from .routes.topic_router import topic_router
from .routes.reply_router import reply_router
from .routes.conversation_router import conversation_router
from .routes.message_router import message_router
from .routes.category_router import category_router


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(category_router)
api_router.include_router(topic_router)
api_router.include_router(reply_router)
api_router.include_router(conversation_router)
api_router.include_router(message_router)
