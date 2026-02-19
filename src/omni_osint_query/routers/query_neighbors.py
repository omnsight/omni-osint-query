import logging
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from omni_python_library.dal.query_tools.entity_neighborhood import (
    search_entity_neighborhood,
)
from omni_python_library.middleware.user_token import get_user_context
from omni_python_library.models.osint import (
    Event,
    Organization,
    Person,
    Relation,
    Source,
    Website,
)
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/query", tags=["query"])


class NeighborsRequest(BaseModel):
    entity_id: str


class NeighborsResponse(BaseModel):
    events: List[Event] = []
    sources: List[Source] = []
    persons: List[Person] = []
    organizations: List[Organization] = []
    websites: List[Website] = []
    relations: List[Relation] = []


@router.post("/neighbors", response_model=NeighborsResponse)
def get_neighbors(request: NeighborsRequest, user_ctx: Dict = Depends(get_user_context)):
    try:
        results = search_entity_neighborhood(
            entity_id=request.entity_id,
            owner=user_ctx["user_id"],
            roles=user_ctx["roles"],
            limit=30,
        )

        return NeighborsResponse(
            events=[e for e in results if isinstance(e, Event)],
            sources=[s for s in results if isinstance(s, Source)],
            persons=[p for p in results if isinstance(p, Person)],
            organizations=[o for o in results if isinstance(o, Organization)],
            websites=[w for w in results if isinstance(w, Website)],
            relations=[r for r in results if isinstance(r, Relation)],
        )
    except Exception as e:
        logger.exception("Error executing neighbors query")
        raise HTTPException(status_code=400, detail=str(e))
