"""Main orchestration script for the micro-influencer outreach pipeline."""
import pandas as pd
import json
import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all modules (after adding parent to path)
from src.influencer_data import get_influencers
from src.hybrid_discovery import run_hybrid_discovery
from src.filter_segments import create_segments, save_segments
from src.profile_enrichment import enrich_all as enrich_profiles, save_enriched_data
from src.message_generator import generate_all_messages, save_messages
from src.sending_layer import (
    explain_email_sending_workflow,
    explain_dm_sending_workflow,
    run_mock_sending_campaign
)


# Auto-run discovery if data file doesn't exist
if not os.path.exists("data/raw/influencers_raw.json"):
    print("Running hybrid discovery to generate influencer data...")
    run_hybrid_discovery(target=50)


def load_influencer_data():
      """Load influencer data from file (always uses hybrid discovery file)."""
      real_data_path = "data/raw/influencers_raw.json"
      with open(real_data_path) as f:
          data = json.load(f)
      print(f"  Loaded {len(data)} influencers from hybrid discovery")
      return pd.DataFrame(data)


def run_pipeline():
    """Runs the complete influencer outreach pipeline."""
    print("=" * 60)
    print("   AUTOMATED MICRO-INFLUENCER OUTREACH SYSTEM")
    print("=" * 60)
    print(f"   Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Stage 1: Load Influencer Data
    print("\n[STAGE 1] Loading influencer data...")
    try:
        influencers_df = load_influencer_data()
        print(f"   ✓ Loaded {len(influencers_df)} influencers")
    except Exception as e:
        print(f"   ✗ Error loading data: {e}")
        return

    # Stage 2: Create Segments
    print("\n[STAGE 2] Creating audience segments...")
    try:
        segments = create_segments(influencers_df)
        save_segments(segments)
        for seg_name, seg_df in segments.items():
            print(f"   ✓ {seg_name}: {len(seg_df)} influencers")
    except Exception as e:
        print(f"   ✗ Error creating segments: {e}")

    # Stage 3: Enrich Profiles
    print("\n[STAGE 3] Enriching influencer profiles...")
    try:
        enriched_df = enrich_profiles(influencers_df)
        save_enriched_data(enriched_df)
        print(f"   ✓ Enriched {len(enriched_df)} profiles")
        priority_counts = enriched_df["outreach_priority"].value_counts()
        print(f"      - High: {priority_counts.get('High', 0)}")
        print(f"      - Medium: {priority_counts.get('Medium', 0)}")
        print(f"      - Low: {priority_counts.get('Low', 0)}")
    except Exception as e:
        print(f"   ✗ Error enriching profiles: {e}")
        return

    # Stage 4: Generate Messages
    print("\n[STAGE 4] Generating AI-powered outreach messages...")
    try:
        messages = generate_all_messages(enriched_df, priority_filter="High")
        save_messages(messages)
        print(f"   ✓ Generated {len(messages)} message sets")
    except Exception as e:
        print(f"   ✗ Error generating messages: {e}")
        return

    # Stage 5: Run Mock Campaign
    print("\n[STAGE 5] Running mock sending campaign...")
    try:
        log_df = run_mock_sending_campaign(messages)
        print(f"   ✓ Campaign complete")
    except Exception as e:
        print(f"   ✗ Error running campaign: {e}")

    # Stage 6: Explain Workflows
    print("\n[STAGE 6] Email Sending Workflow:")
    try:
        email_wf = explain_email_sending_workflow()
        print(f"   Method: {email_wf['method']}")
        print(f"   API: {email_wf['api_used']}")
        print(f"   Endpoint: {email_wf['endpoint']}")
        print(f"   Rate Limit: {email_wf['rate_limit']}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    print("\n[STAGE 7] Instagram DM Sending Workflow:")
    try:
        dm_wf = explain_dm_sending_workflow()
        print(f"   Method: {dm_wf['method']}")
        print(f"   API: {dm_wf['api_used']}")
        print(f"   Endpoint: {dm_wf['endpoint']}")
        print(f"   Limitation: {dm_wf['limitation']}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # Final Summary
    print("\n" + "=" * 60)
    print("   CAMPAIGN SUMMARY")
    print("=" * 60)

    try:
        # Load the sent log
        log_df = pd.read_csv("outputs/sent_log/sent_log.csv")

        # Create summary table
        summary_data = []
        for msg in messages:
            email_log = log_df[(log_df["id"] == msg["id"]) & (log_df["channel"] == "email")]
            dm_log = log_df[(log_df["id"] == msg["id"]) & (log_df["channel"] == "instagram_dm")]

            summary_data.append({
                "Influencer Name": msg["name"],
                "Handle": msg["handle"],
                "Priority": msg["outreach_priority"],
                "Email Status": "sent" if len(email_log) > 0 else "pending",
                "DM Status": "sent" if len(dm_log) > 0 else "pending"
            })

        summary_df = pd.DataFrame(summary_data)
        print("\n" + summary_df.to_string(index=False))

        # Save final summary
        os.makedirs("outputs", exist_ok=True)
        summary_df.to_csv("outputs/campaign_summary.csv", index=False)
        print(f"\n✓ Summary saved to outputs/campaign_summary.csv")

    except Exception as e:
        print(f"   ✗ Error creating summary: {e}")

    print("\n" + "=" * 60)
    print(f"   Pipeline completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    run_pipeline()