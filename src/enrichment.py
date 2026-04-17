"""Profile enrichment logic."""
import pandas as pd
import json
import os
from datetime import date


def calculate_estimated_reach(row):
    """Returns estimated people who actively engage per post."""
    return int(row["followers"] * row["engagement_rate"] / 100)


def classify_tier(followers):
    """Returns tier label: Nano (<10k), Micro (10k-50k), Mid-Micro (50k-100k)."""
    if followers < 10000:
        return "Nano"
    elif followers < 50000:
        return "Micro"
    else:
        return "Mid-Micro"


def generate_collaboration_score(row):
    """Score out of 100 based on brand_fit, engagement, platform, and language."""
    score = 0

    # brand_fit_score * 5 (max 50)
    score += row["brand_fit_score"] * 5

    # engagement_rate * 4 (max 34 if capped at 8.5)
    score += row["engagement_rate"] * 4

    # +10 if platform includes "Instagram"
    if "Instagram" in row["platform"]:
        score += 10

    # +6 if language in ["Hinglish", "English"]
    if row["language"] in ["Hinglish", "English"]:
        score += 6

    return round(score, 2)


def enrich_influencer(row):
    """Enriches a single row with additional fields."""
    from datetime import date as dt

    estimated_reach = calculate_estimated_reach(row)
    tier = classify_tier(row["followers"])
    collaboration_score = generate_collaboration_score(row)
    content_theme_summary = " | ".join(row["content_themes"])

    if collaboration_score >= 70:
        outreach_priority = "High"
    elif collaboration_score >= 50:
        outreach_priority = "Medium"
    else:
        outreach_priority = "Low"

    enriched = row.to_dict()
    enriched["estimated_reach"] = estimated_reach
    enriched["tier"] = tier
    enriched["collaboration_score"] = collaboration_score
    enriched["content_theme_summary"] = content_theme_summary
    enriched["outreach_priority"] = outreach_priority
    enriched["enriched_at"] = str(dt.today())

    return enriched


def enrich_all(df):
    """Applies enrich_influencer to all rows, returns enriched DataFrame."""
    enriched_rows = [enrich_influencer(row) for _, row in df.iterrows()]
    return pd.DataFrame(enriched_rows)


def save_enriched_data(df):
    """Saves enriched data to CSV and JSON, prints summary."""
    os.makedirs("data/enriched", exist_ok=True)

    csv_path = "data/enriched/influencers_enriched.csv"
    json_path = "data/enriched/influencers_enriched.json"

    df.to_csv(csv_path, index=False)
    with open(json_path, "w") as f:
        json.dump(df.to_dict(orient="records"), f, indent=2)

    # Summary
    total = len(df)
    priority_counts = df["outreach_priority"].value_counts().to_dict()
    avg_score = df["collaboration_score"].mean()

    print(f"Total enriched: {total}")
    print(f"High priority: {priority_counts.get('High', 0)}")
    print(f"Medium priority: {priority_counts.get('Medium', 0)}")
    print(f"Low priority: {priority_counts.get('Low', 0)}")
    print(f"Average collaboration score: {avg_score:.2f}")


if __name__ == "__main__":
    import pandas as pd
    from src.influencer_data import get_influencers

    df = pd.DataFrame(get_influencers())
    enriched_df = enrich_all(df)
    save_enriched_data(enriched_df)