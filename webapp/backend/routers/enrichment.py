"""Enrichment router - /api/enrich endpoint."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import APIRouter, HTTPException
from models import FilterRequest
import json
import pandas as pd

router = APIRouter()


@router.post("/enrich")
async def enrich_profiles(filter_request: FilterRequest):
    """Load raw data, apply filters, enrich all profiles"""
    try:
        from src.profile_enrichment import enrich_all

        # Also import filter functions from our existing code
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        raw_path = os.path.join(project_root, "data/raw/influencers_raw.json")

        with open(raw_path) as f:
            data = json.load(f)

        df = pd.DataFrame(data)

        # Apply filters from request
        if filter_request.min_engagement or filter_request.max_engagement:
            min_eng = filter_request.min_engagement or 0
            max_eng = filter_request.max_engagement or 100
            df = df[(df["engagement_rate"] >= min_eng) & (df["engagement_rate"] <= max_eng)]

        if filter_request.min_brand_fit:
            df = df[df["brand_fit_score"] >= filter_request.min_brand_fit]

        if filter_request.platforms:
            df = df[df["platform"].isin(filter_request.platforms)]

        if filter_request.niches:
            df = df[df["niche"].isin(filter_request.niches)]

        if filter_request.cities:
            df = df[df["city"].isin(filter_request.cities)]

        # Enrich
        enriched_df = enrich_all(df)

        # Save
        enriched_dir = os.path.join(project_root, "data/enriched")
        os.makedirs(enriched_dir, exist_ok=True)
        enriched_df.to_csv(os.path.join(enriched_dir, "influencers_enriched.csv"), index=False)
        enriched_df.to_json(os.path.join(enriched_dir, "influencers_enriched.json"), orient="records", indent=2)

        return {
            "total": len(enriched_df),
            "high_priority": len(enriched_df[enriched_df["outreach_priority"] == "High"]) if "outreach_priority" in enriched_df else 0,
            "medium_priority": len(enriched_df[enriched_df["outreach_priority"] == "Medium"]) if "outreach_priority" in enriched_df else 0,
            "low_priority": len(enriched_df[enriched_df["outreach_priority"] == "Low"]) if "outreach_priority" in enriched_df else 0,
            "avg_collaboration_score": round(enriched_df["collaboration_score"].mean(), 2) if "collaboration_score" in enriched_df else 0,
            "influencers": enriched_df.to_dict(orient="records")
        }

    except Exception as e:
        return {"error": str(e)}