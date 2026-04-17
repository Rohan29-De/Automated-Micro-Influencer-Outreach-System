# Automated Micro-Influencer Outreach System

A Python-based system for identifying, enriching, and reaching out to micro-influencers for marketing campaigns.

## Structure

```
micro_influencer_outreach/
├── data/
│   ├── raw/           # Raw influencer data
│   └── enriched/      # Enriched profiles
├── outputs/
│   ├── segments/      # Filtered segments
│   └── messages/      # Generated outreach messages
├── src/
│   ├── influencer_data.py   # 50 influencer records
│   ├── filter.py            # Filtering & segmentation logic
│   ├── enrichment.py        # Profile enrichment logic
│   ├── message_generator.py # Message generation using Anthropic API
│   └── sending_layer.py     # Outreach execution & mock API flow
├── main.py            # Pipeline orchestrator
├── requirements.txt   # Python dependencies
└── .env              # Environment variables
```

## Setup

```bash
pip install -r requirements.txt
cp .env .env.local  # Add your ANTHROPIC_API_KEY
```

## Usage

```bash
python main.py
```

