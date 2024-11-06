import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from forum_system_api.api.api_v1.api import api_router
from forum_system_api.persistence.database import initialize_database


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


if __name__ == "__main__":
    initialize_database()
    uvicorn.run("forum_system_api.main:app", host="127.0.0.1", port=8000, reload=True)
