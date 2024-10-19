import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from forum_system_api.api.api_v1.api import api_router
from forum_system_api.persistence.database import create_tables

create_tables()

app = FastAPI()

app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


if __name__ == "__main__":
    uvicorn.run("forum_system_api.main:app", host="127.0.0.1", port=8000, reload=True)
