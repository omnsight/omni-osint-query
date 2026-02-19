from contextlib import asynccontextmanager

from fastapi import FastAPI
from omni_python_library import init_omni_library

from omni_osint_query.routers import (
    health_router,
    neighbors_router,
    query_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_omni_library()
    yield


app = FastAPI(title="Omni OSINT Query", lifespan=lifespan)

# Include routers
app.include_router(query_router)
app.include_router(neighbors_router)
app.include_router(health_router)
