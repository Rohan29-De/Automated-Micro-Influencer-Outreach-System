"""Discovery router - /api/discover endpoint."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import APIRouter, BackgroundTasks
from models import DiscoveryRequest, InfluencerProfile
import json

router = APIRouter()

# In-memory state (simple, no DB needed)
discovery_state = {
    "status": "idle",  # idle | running | complete | error
    "progress": 0,
    "total": 50,
    "influencers": [],
    "message": ""
}


@router.post("/discover")
async def start_discovery(request: DiscoveryRequest, background_tasks: BackgroundTasks):
    """Start influencer discovery in background"""
    discovery_state["status"] = "running"
    discovery_state["progress"] = 0
    discovery_state["influencers"] = []
    discovery_state["message"] = f"Discovering {request.niche} influencers on {request.platform}..."

    background_tasks.add_task(run_discovery, request)

    return {"message": "Discovery started", "status": "running"}


@router.get("/discover/status")
async def get_discovery_status():
    """Poll this endpoint to get real-time discovery progress"""
    return discovery_state


@router.get("/discover/results")
async def get_discovery_results():
    """Get final list of discovered influencers - reads directly from file"""
    # Hardcoded absolute path for reliability
    raw_path = "/home/rohan/micro_influencer_outreach/data/raw/influencers_raw.json"

    if os.path.exists(raw_path):
        with open(raw_path) as f:
            data = json.load(f)

        # Update state
        discovery_state["status"] = "complete"
        discovery_state["influencers"] = data
        discovery_state["message"] = f"Found {len(data)} influencers"

        return {"count": len(data), "influencers": data}

    return {"count": 0, "influencers": []}


async def run_discovery(request: DiscoveryRequest):
    """Background task: runs hybrid discovery with niche/platform params"""
    try:
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        from src.hybrid_discovery import run_hybrid_discovery

        discovery_state["message"] = f"Searching for {request.niche} creators..."
        discovery_state["progress"] = 10

        profiles = run_hybrid_discovery(
            target=request.target_count,
            niche=request.niche,
            platform=request.platform
        )

        discovery_state["status"] = "complete"
        discovery_state["progress"] = 100
        discovery_state["influencers"] = profiles
        discovery_state["message"] = f"Found {len(profiles)} influencers!"

    except Exception as e:
        discovery_state["status"] = "error"
        discovery_state["message"] = str(e)