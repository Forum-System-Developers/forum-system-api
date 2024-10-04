from fastapi import FastAPI

from forum_system_api.api.api_v1.api import api_router
from forum_system_api.persistence.database import create_tables


create_tables()

app = FastAPI()
app.include_router(api_router)

# uvicorn forum_system_api.main:app --reload