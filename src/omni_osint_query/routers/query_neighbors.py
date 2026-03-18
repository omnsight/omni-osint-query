import logging
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from omni_python_library.dal.query_tools import (
    search_entity_neighborhood,
)
from omni_python_library.middleware import get_user_context
from omni_python_library.models import (
    Event,
    Organization,
    Person,
    Relation,
    Source,
    Website,
)
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/query", tags=["query"])


class NeighborsRequest(BaseModel):
    entity_id: str = Field(description="The ID of the entity to query for neighbors.")
    limit: int = Field(default=30, description="The maximum number of results to return.")
    offset: int = Field(default=0, description="The offset from which to start returning results.")


class NeighborsResponse(BaseModel):
    events: List[Event] = Field(default_factory=list, description="A list of events related to the entity.")
    sources: List[Source] = Field(default_factory=list, description="A list of sources related to the entity.")
    persons: List[Person] = Field(default_factory=list, description="A list of persons related to the entity.")
    organizations: List[Organization] = Field(
        default_factory=list, description="A list of organizations related to the entity."
    )
    websites: List[Website] = Field(default_factory=list, description="A list of websites related to the entity.")
    relations: List[Relation] = Field(default_factory=list, description="A list of relations related to the entity.")
    offset: int = Field(default=0, description="The offset from which to start returning results.")


@router.post("/neighbors", response_model=NeighborsResponse, operation_id="query_neighbors")
def query_neighbors(request: NeighborsRequest, user_ctx: Dict = Depends(get_user_context)):
    try:
        results = search_entity_neighborhood(
            entity_id=request.entity_id,
            owner=user_ctx["user_id"],
            roles=user_ctx["roles"],
            limit=request.limit,
            offset=request.offset,
        )

        return NeighborsResponse(
            events=[e for e in results if isinstance(e, Event)],
            sources=[s for s in results if isinstance(s, Source)],
            persons=[p for p in results if isinstance(p, Person)],
            organizations=[o for o in results if isinstance(o, Organization)],
            websites=[w for w in results if isinstance(w, Website)],
            relations=[r for r in results if isinstance(r, Relation)],
            offset=request.offset + len(results),
        )
    except Exception:
        logger.exception("Error executing neighbors query")
        raise HTTPException(status_code=500, detail="Internal server error")
