from fastapi import FastAPI

from forum_system_api.persistence.database import create_tables
from forum_system_api.routers.topic_router import topic_router


create_tables()

app = FastAPI()
app.include_router(topic_router)

# uvicorn forum_system_api.main:app --reload