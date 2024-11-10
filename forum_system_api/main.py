import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from forum_system_api.api.api_v1.api import api_router
from forum_system_api.persistence.database import initialize_database


app = FastAPI()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

initialize_database()
