from ..schemas.common import FilterParams
from ..persistence.models.topic import Topic
from ..schemas.topic import TopicResponse
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

def get_all(filter_params: FilterParams, db: Session) -> list[TopicResponse]:
    query = (
        db.query(Topic)
        .offset(filter_params.offset)
        .limit(filter_params.limit)
    )
    
    if filter_params.order == 'asc':
        query = query.order_by(asc(getattr(Topic, filter_params.order_by)))
    else:
        query = query.order_by(desc(getattr(Topic, filter_params.order_by)))

    topics = query.all()
    
    return topics
