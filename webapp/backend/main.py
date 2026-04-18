"""FastAPI application entry point."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import APP_NAME
from routers import discovery, enrichment, segments, messages


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load .env on startup."""
    # TODO: Load any cached data here
    yield


app = FastAPI(
    title=APP_NAME,
    description="Micro-Influencer Outreach System API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS for frontend on localhost:5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with /api prefix
app.include_router(discovery.router, prefix="/api")
app.include_router(enrichment.router, prefix="/api")
app.include_router(segments.router, prefix="/api")
app.include_router(messages.router, prefix="/api")


@app.get("/")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "app": "Micro-Influencer Outreach System"}


@app.get("/health")
async def detailed_health():
    """Detailed health check."""
    return {
        "status": "healthy",
        "api": "running",
        "endpoints": {
            "discover": "/api/discover",
            "enrich": "/api/enrich",
            "segments": "/api/segments",
            "messages": "/api/messages"
        }
    }