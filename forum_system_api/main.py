import uvicorn
from fastapi import FastAPI

from forum_system_api.api.api_v1.api import api_router
from forum_system_api.persistence.database import create_tables

create_tables()

app = FastAPI()

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("forum_system_api.main:app", host="127.0.0.1", port=8000, reload=True)

# category id: 15fef349-8e42-44bb-a649-e30a422b4018
# user id ed834a53-7e0b-47d0-ba0e-920840c70d40
# admin  f6dce522-5006-4340-a8f3-ee66b1468b15
