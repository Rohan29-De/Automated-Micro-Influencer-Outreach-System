"""Messages router - /api/messages endpoint."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import APIRouter, HTTPException
from models import MessageRequest, MessageResponse
import json
import pandas as pd

router = APIRouter()


@router.post("/messages/generate-one")
async def generate_one_message(request: MessageRequest):
    """Generate email + DM for a single influencer"""
    try:
        from src.message_generator import generate_all_messages

        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        enriched_path = os.path.join(project_root, "data/enriched/influencers_enriched.json")

        with open(enriched_path) as f:
            data = json.load(f)

        influencer = next((x for x in data if x.get("id") == request.influencer_id), None)

        if not influencer:
            return {"error": f"Influencer {request.influencer_id} not found"}

        # Create a DataFrame with single row
        df = pd.DataFrame([influencer])

        # Override brand name and collaboration type in the data
        df["brand_name"] = request.brand_name
        df["collaboration_type"] = request.collaboration_type

        messages = generate_all_messages(df, priority_filter=None)

        if messages:
            return messages[0]
        return {"error": "Failed to generate message"}

    except Exception as e:
        return {"error": str(e)}


@router.post("/messages/generate-all")
async def generate_all_messages(priority: str = "High"):
    """Generate messages for all influencers of given priority"""
    try:
        from src.message_generator import generate_all_messages, save_messages

        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        enriched_path = os.path.join(project_root, "data/enriched/influencers_enriched.csv")

        df = pd.read_csv(enriched_path)

        messages = generate_all_messages(df, priority_filter=priority)

        save_messages(messages)

        return {"generated": len(messages), "messages": messages}

    except Exception as e:
        return {"error": str(e)}


@router.get("/messages/results")
async def get_messages():
    """Get all previously generated messages"""
    try:
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        path = os.path.join(project_root, "outputs/messages/outreach_messages.json")

        if not os.path.exists(path):
            return {"count": 0, "messages": []}

        with open(path) as f:
            messages = json.load(f)

        return {"count": len(messages), "messages": messages}

    except Exception as e:
        return {"error": str(e)}