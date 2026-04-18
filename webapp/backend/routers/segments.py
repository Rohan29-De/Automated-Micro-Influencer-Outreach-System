"""Segments router - /api/segments endpoint."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import APIRouter, HTTPException
import json
import pandas as pd

router = APIRouter()


@router.get("/segments")
async def get_segments():
    """Create and return all 3 segments from enriched data"""
    try:
        from src.filter_segments import create_segments

        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        enriched_path = os.path.join(project_root, "data/enriched/influencers_enriched.csv")

        if not os.path.exists(enriched_path):
            return {"error": "Run enrichment first"}

        df = pd.read_csv(enriched_path)

        # Ensure required columns exist
        required_cols = ["engagement_rate", "brand_fit_score", "followers"]
        for col in required_cols:
            if col not in df.columns:
                return {"error": f"Missing column: {col}. Run enrichment first."}

        segments = create_segments(df)

        result = {}
        for name, seg_df in segments.items():
            result[name] = {
                "count": len(seg_df),
                "influencers": seg_df.to_dict(orient="records")
            }

        return result

    except Exception as e:
        return {"error": str(e)}