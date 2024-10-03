from fastapi import APIRouter

from .routes.topic_router import topic_router

api_router = APIRouter(prefix='/api/v1')

api_router.include_router(topic_router)
