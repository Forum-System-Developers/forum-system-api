from typing import Literal
from pydantic import BaseModel, Field


class FilterParams(BaseModel):
    order: Literal['asc', 'desc'] = 'asc'
    order_by: Literal['name', 'title', 'created_at'] = 'created_at'
    limit: int = Field(20, gt=0, le=100)
    offset: int = Field(0, ge=0)