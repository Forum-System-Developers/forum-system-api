from fastapi import APIRouter

from .routes.user_router import router as user_router
from .routes.topic_router import topic_router
from .routes.reply_router import reply_router


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(user_router)
api_router.include_router(topic_router)
api_router.include_router(reply_router)



