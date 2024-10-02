from fastapi import FastAPI

from forum_system_api.persistence.database import create_tables


create_tables()

app = FastAPI()
