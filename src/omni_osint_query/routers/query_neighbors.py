import logging
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from omni_python_library.dal.osint_data_access_layer import OsintDataAccessLayer
from omni_python_library.dal.query_tools import search_entity_neighborhood
from omni_python_library.middleware import get_user_context
from omni_python_library.models import (
    Event,
    Organization,
    Person,
    Relation,
    Source,
    Website,
)
from omni_python_library.utils.config import ArangoDBConstant
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(tags=["query"])


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


@router.get("/entities/{id:path}/neighbors", response_model=NeighborsResponse, operation_id="query_neighbors")
def query_neighbors(
    id: str = Path(
        pattern=r"^[A-Za-z0-9_-]+\/[A-Za-z0-9_-]+$", description="The ArangoDB Document ID (e.g., collection/123)"
    ),
    user_ctx: Dict = Depends(get_user_context),
    limit: int = Query(default=30, description="The maximum number of results to return."),
    offset: int = Query(default=0, description="The offset from which to start returning results."),
    include: List[str] = Query(default=None, description="A list of entity types to include."),
    exclude: List[str] = Query(default=None, description="A list of entity types to exclude."),
):
    try:
        logger.info(f"Querying neighbors of entity: {id}")
        results = search_entity_neighborhood(
            entity_id=id,
            owner=user_ctx["user_id"],
            roles=user_ctx["roles"],
            limit=limit,
            offset=offset,
        )

        if include:
            results = [r for r in results if type(r).__name__ in include or isinstance(r, Relation)]
        if exclude:
            results = [r for r in results if type(r).__name__ not in exclude or isinstance(r, Relation)]

        filtered_results = [r for r in results if not isinstance(r, Relation)]
        result_ids = {r.id for r in filtered_results}
        result_ids.add(id)

        return NeighborsResponse(
            events=[e for e in results if isinstance(e, Event)],
            sources=[s for s in results if isinstance(s, Source)],
            persons=[p for p in results if isinstance(p, Person)],
            organizations=[o for o in results if isinstance(o, Organization)],
            websites=[w for w in results if isinstance(w, Website)],
            relations=[
                r for r in results if isinstance(r, Relation) and r.from_id in result_ids and r.to_id in result_ids
            ],
            offset=offset + len(results),
        )
    except Exception:
        logger.exception("Error executing neighbors query")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/entities/neighbors", response_model=NeighborsResponse, operation_id="query_neighbors_batch")
def query_neighbors_batch(
    ids: List[str] = Query(
        default_factory=list, max_length=100, description="A list of entity IDs to query neighbors for."
    ),
    user_ctx: Dict = Depends(get_user_context),
    limit: int = Query(default=30, description="The maximum number of results to return."),
    offset: int = Query(default=0, description="The offset from which to start returning results."),
    include: List[str] = Query(default=None, description="A list of entity types to include."),
    exclude: List[str] = Query(default=None, description="A list of entity types to exclude."),
):
    try:
        logger.info(f"Querying neighbors of entities: {ids}")
        bind_vars = {
            "entity_ids": ids,
            "limit": limit,
            "offset": offset,
            "owner": user_ctx["user_id"],
            "roles": user_ctx["roles"],
        }

        query = f"""
            LET all_neighbors = (
                FOR entity_id IN @entity_ids
                    FOR v, e IN 1..1 ANY entity_id GRAPH '{ArangoDBConstant.EVENT_RELATED_GRAPH}'
                        FILTER v.owner == @owner OR (FOR r IN @roles FILTER r IN v.read LIMIT 1 RETURN true)[0]
                        RETURN {{ v: v, e: e }}
            )
            LET limited_neighbors = (
                FOR n IN all_neighbors
                    LIMIT @offset, @limit
                    RETURN n
            )
            LET vertices = (FOR t IN limited_neighbors RETURN t.v)
            LET edges = (FOR t IN limited_neighbors RETURN t.e)
            RETURN {{ nodes: vertices, edges: edges }}
        """

        all_results = OsintDataAccessLayer().query(query, bind_vars=bind_vars, in_pending=False)

        unique_results = {r.id: r for r in all_results}.values()

        if include:
            unique_results = [r for r in unique_results if type(r).__name__ in include or isinstance(r, Relation)]
        if exclude:
            unique_results = [r for r in unique_results if type(r).__name__ not in exclude or isinstance(r, Relation)]

        filtered_results = [r for r in unique_results if not isinstance(r, Relation)]
        result_ids = {r.id for r in filtered_results}
        result_ids.update(ids)

        return NeighborsResponse(
            events=[e for e in unique_results if isinstance(e, Event)],
            sources=[s for s in unique_results if isinstance(s, Source)],
            persons=[p for p in unique_results if isinstance(p, Person)],
            organizations=[o for o in unique_results if isinstance(o, Organization)],
            websites=[w for w in unique_results if isinstance(w, Website)],
            relations=[
                r
                for r in unique_results
                if isinstance(r, Relation) and r.from_id in result_ids and r.to_id in result_ids
            ],
            offset=offset + len(list(unique_results)),
        )
    except Exception:
        logger.exception("Error executing neighbors query")
        raise HTTPException(status_code=500, detail="Internal server error")
