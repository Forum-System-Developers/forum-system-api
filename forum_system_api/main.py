import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from forum_system_api.api.api_v1.api import api_router
from forum_system_api.persistence.database import create_tables

create_tables()

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("forum_system_api.main:app", host="127.0.0.1", port=8000, reload=True)