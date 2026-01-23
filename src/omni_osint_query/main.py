from fastapi import FastAPI
from contextlib import asynccontextmanager
import os
from omni_osint_query.routers import (
    query_router,
    neighbors_router,
    health_router,
)
from omni_python_library import init_omni_library


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_omni_library()
    yield


app = FastAPI(title="Omni OSINT Query", lifespan=lifespan)

# Include routers
app.include_router(query_router)
app.include_router(neighbors_router)
app.include_router(health_router)
