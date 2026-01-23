from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Optional
from pydantic import BaseModel
from omni_python_library.dal.osint_data_access_layer import OsintDataAccessLayer
from omni_python_library.dal.query_tools.event_search import search_events
from omni_python_library.middleware.user_token import get_user_context
from omni_python_library.models.osint import (
    Event,
    Relation,
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/query", tags=["query"])
dal = OsintDataAccessLayer()


class QueryRequest(BaseModel):
    query: Optional[str] = None
    date_start: Optional[int] = None
    date_end: Optional[int] = None
    country_code: Optional[str] = None


class QueryResponse(BaseModel):
    events: List[Event] = []
    relations: List[Relation] = []


@router.post("/query_events", response_model=QueryResponse)
def execute_query(request: QueryRequest, user_ctx: Dict = Depends(get_user_context)):
    try:
        results = search_events(
            text=request.query,
            date_range=(request.date_start, request.date_end),
            country_code=request.country_code,
            limit=100,
        )

        return QueryResponse(
            events=[e for e in results if isinstance(e, Event)],
            relations=[r for r in results if isinstance(r, Relation)],
        )
    except Exception as e:
        logger.exception("Error executing query")
        raise HTTPException(status_code=400, detail=str(e))
