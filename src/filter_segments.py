"""Filtering and segmentation logic."""
import pandas as pd
import os


def filter_by_engagement(df, min_rate=2.0, max_rate=8.5):
    """Returns influencers within the engagement rate range."""
    return df[(df["engagement_rate"] >= min_rate) & (df["engagement_rate"] <= max_rate)]


def filter_by_platform(df, platform):
    """Filter by platform. For 'Instagram' also includes 'Instagram+YouTube'."""
    if platform == "Instagram":
        return df[df["platform"].isin(["Instagram", "Instagram+YouTube"])]
    return df[df["platform"] == platform]


def filter_by_niche(df, niches: list):
    """Filter by one or more niche values."""
    return df[df["niche"].isin(niches)]


def filter_by_city(df, cities: list):
    """Filter by one or more Indian cities."""
    return df[df["city"].isin(cities)]


def filter_by_brand_fit(df, min_score=7):
    """Only return influencers with brand_fit_score >= min_score."""
    return df[df["brand_fit_score"] >= min_score]


def create_segments(df):
    """Create and return exactly 3 segments as separate DataFrames."""
    segments = {}

    # Segment A — "Instagram Beauty & Skincare Stars"
    seg_a = df[
        (df["platform"].isin(["Instagram", "Instagram+YouTube"])) &
        (df["niche"].isin(["Beauty", "Skincare", "Makeup"])) &
        (df["engagement_rate"] >= 3.0) &
        (df["brand_fit_score"] >= 6)
    ]
    segments["Segment_A"] = seg_a

    # Segment B — "YouTube Fashion Content Creators"
    seg_b = df[
        (df["platform"].isin(["YouTube", "Instagram+YouTube"])) &
        (df["niche"].isin(["Fashion", "Lifestyle+Fashion"])) &
        (df["engagement_rate"] >= 2.5) &
        (df["brand_fit_score"] >= 5)
    ]
    segments["Segment_B"] = seg_b

    # Segment C — "High Engagement Hindi/Hinglish Creators"
    seg_c = df[
        (df["language"].isin(["Hindi", "Hinglish"])) &
        (df["engagement_rate"] >= 4.0) &
        (df["brand_fit_score"] >= 7)
    ]
    segments["Segment_C"] = seg_c

    return segments


def save_segments(segments: dict):
    """Save each segment as CSV in outputs/segments/."""
    os.makedirs("outputs/segments", exist_ok=True)

    for name, df in segments.items():
        filepath = f"outputs/segments/{name}.csv"
        df.to_csv(filepath, index=False)
        print(f"{name}: {len(df)} influencers saved to {filepath}")


if __name__ == "__main__":
    import pandas as pd
    from src.influencer_data import get_influencers

    df = pd.DataFrame(get_influencers())
    segments = create_segments(df)
    save_segments(segments)