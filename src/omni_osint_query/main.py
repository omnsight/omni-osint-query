import logging
import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from omni_python_library import init_omni_library

from omni_osint_query.routers import (
    health_router,
    neighbors_router,
    query_router,
)

# Configure logging
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
log_level = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(stream=sys.stdout, level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")
    init_omni_library()
    yield
    logger.info("Application shutdown")


app = FastAPI(title="Omni OSINT Query", lifespan=lifespan)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


# Include routers
app.include_router(query_router)
app.include_router(neighbors_router)
app.include_router(health_router)
