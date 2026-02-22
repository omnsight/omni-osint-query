import logging
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from omni_python_library.dal.query_tools import search_events
from omni_python_library.middleware import get_user_context
from omni_python_library.models import (
    Event,
    Relation,
)
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/query", tags=["query"])


class QueryRequest(BaseModel):
    query: Optional[str] = Field(default=None, description="The search query string.")
    date_start: Optional[int] = Field(default=None, description="The start of the date range for the query.")
    date_end: Optional[int] = Field(default=None, description="The end of the date range for the query.")
    country_code: Optional[str] = Field(default=None, description="The country code to filter the query by.")
    limit: int = Field(default=30, description="The maximum number of results to return.")
    offset: int = Field(default=0, description="The offset from which to start returning results.")


class QueryResponse(BaseModel):
    events: List[Event] = Field(default_factory=list, description="A list of events that match the query.")
    relations: List[Relation] = Field(default_factory=list, description="A list of relations that match the query.")


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
