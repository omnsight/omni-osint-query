import logging
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from omni_python_library.dal.query_tools import search_events
from omni_python_library.middleware import get_user_context
from omni_python_library.models import (
    Event,
    Relation,
)
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(tags=["query"])


class QueryResponse(BaseModel):
    events: List[Event] = Field(default_factory=list, description="A list of events that match the query.")
    relations: List[Relation] = Field(default_factory=list, description="A list of relations that match the query.")
    offset: int = Field(default=0, description="The offset from which to start returning results.")


@router.get("/events/query", response_model=QueryResponse, operation_id="query_events")
def query_events(
    query: Optional[str] = Query(default=None, description="The search query string."),
    date_start: Optional[int] = Query(default=None, description="The start of the date range for the query."),
    date_end: Optional[int] = Query(default=None, description="The end of the date range for the query."),
    country_code: Optional[str] = Query(default=None, description="The country code to filter the query by."),
    limit: int = Query(default=30, description="The maximum number of results to return."),
    offset: int = Query(default=0, description="The offset from which to start returning results."),
    user_ctx: Dict = Depends(get_user_context),
):
    try:
        logger.info(
            f"Querying events with request: query={query}, date_start={date_start}, date_end={date_end}, "
            f"country_code={country_code}, limit={limit}, offset={offset}"
        )
        results = search_events(
            owner=user_ctx["user_id"],
            roles=user_ctx["roles"],
            text=query,
            date_range=(date_start, date_end),
            country_code=country_code,
            limit=limit,
            offset=offset,
        )

        return QueryResponse(
            events=[e for e in results if isinstance(e, Event)],
            relations=[r for r in results if isinstance(r, Relation)],
            offset=offset + len(results),
        )
    except Exception:
        logger.exception("Error executing query")
        raise HTTPException(status_code=500, detail="Internal server error")
