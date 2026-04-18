# Automated Micro-Influencer Outreach System

An end-to-end pipeline for identifying, segmenting, enriching, and reaching out to Indian Beauty/Fashion micro-influencers using AI-powered message generation.

## Overview

This system automates the influencer outreach process for brands in the Beauty/Fashion space. It generates realistic micro-influencer data, segments audiences, enriches profiles with engagement metrics, creates personalized email/DM pitches using Groq AI, and provides a mock sending layer for campaign execution.

## Tech Stack

- **Python 3.14** - Core language
- **Groq API** - AI-powered message generation (Llama 3.1 model)
- **Pandas** - Data manipulation
- **SendGrid API** - Email sending (production)
- **Instagram Graph API** - DM sending (production)
- **python-dotenv** - Environment variable management

## Folder Structure

```
micro_influencer_outreach/
├── .env                      # API keys (not committed)
├── .env.example              # Environment variable template
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── data/
│   ├── raw/                  # Raw influencer data (CSV/JSON)
│   └── enriched/             # Enriched profile data
├── outputs/
│   ├── segments/             # Audience segment CSVs
│   ├── messages/             # Generated outreach messages
│   ├── sent_log/             # Campaign sending log
│   └── campaign_summary.csv  # Final campaign summary
└── src/
    ├── main.py               # Pipeline orchestration
    ├── influencer_data.py    # Generate 50 fake influencers
    ├── filter_segments.py    # Filtering & segmentation logic
    ├── profile_enrichment.py # Profile enrichment (tiers, scores)
    ├── message_generator.py  # AI pitch generation (Groq)
    └── sending_layer.py      # Mock campaign + workflow docs
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys:
   # - GROQ_API_KEY (required)
   # - SENDGRID_API_KEY (for production email)
   # - INSTAGRAM_ACCESS_TOKEN (for production DMs)
   ```

## How to Run

```bash
python src/main.py
```

## Pipeline Stages (Prompt 1-7)

| Stage | Module | Description |
|-------|--------|-------------|
| 1 | `influencer_data.py` | Generate 50 realistic Indian Beauty/Fashion micro-influencers |
| 2 | `filter_segments.py` | Filter by engagement, platform, niche, city, brand fit; create 3 segments |
| 3 | `profile_enrichment.py` | Add estimated reach, tier classification, collaboration scores |
| 4 | `message_generator.py` | Generate AI-powered email & DM pitches using Groq |
| 5 | `sending_layer.py` | Mock campaign execution + workflow documentation |
| 6 | `sending_layer.py` | Display email & DM API workflow explanations |
| 7 | `main.py` | Orchestrate all stages, display summary table |

## Sample Output

```
============================================================
   AUTOMATED MICRO-INFLUENCER OUTREACH SYSTEM
============================================================
   Started at: 2025-01-15 10:30:00
============================================================

[STAGE 1] Loading influencer data...
   ✓ Loaded 50 influencers

[STAGE 2] Creating audience segments...
   ✓ Segment_A: 21 influencers
   ✓ Segment_B: 12 influencers
   ✓ Segment_C: 14 influencers

[STAGE 3] Enriching influencer profiles...
   ✓ Enriched 50 profiles
      - High: 24
      - Medium: 24
      - Low: 2

[STAGE 4] Generating AI-powered outreach messages...
   ✓ Generated 24 message sets

[STAGE 5] Running mock sending campaign...
   ✓ Campaign complete
...
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | API key for Groq LLM service | Yes |
| `SENDGRID_API_KEY` | API key for SendGrid email service | No (production) |
| `INSTAGRAM_ACCESS_TOKEN` | Meta access token for Instagram API | No (production) |

## License

MIT