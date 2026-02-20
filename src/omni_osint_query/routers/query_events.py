import logging
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from omni_python_library.dal.query_tools.event_search import search_events
from omni_python_library.middleware.user_token import get_user_context
from omni_python_library.models.osint import (
    Event,
    Relation,
)
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/query", tags=["query"])


class QueryRequest(BaseModel):
    query: Optional[str] = None
    date_start: Optional[int] = None
    date_end: Optional[int] = None
    country_code: Optional[str] = None


class QueryResponse(BaseModel):
    events: List[Event] = []
    relations: List[Relation] = []


@router.post("/events", response_model=QueryResponse, operation_id="query_events")
def query_events(request: QueryRequest, user_ctx: Dict = Depends(get_user_context)):
    try:
        results = search_events(
            owner=user_ctx["user_id"],
            roles=user_ctx["roles"],
            text=request.query,
            date_range=(request.date_start, request.date_end),
            country_code=request.country_code,
            limit=30,
        )

        return QueryResponse(
            events=[e for e in results if isinstance(e, Event)],
            relations=[r for r in results if isinstance(r, Relation)],
        )
    except Exception:
        logger.exception("Error executing query")
        raise HTTPException(status_code=500, detail="Internal server error")
