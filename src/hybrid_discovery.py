"""Hybrid discovery: Combines real YouTube API data with smart gap-filling."""
import os
import sys
import time
import random
import csv
import json
from typing import List, Dict, Optional

import requests

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from src.youtube_discovery import (
    get_channel_details,
    extract_channel_id,
    get_recent_videos,
    build_influencer_profile,
    INDIA_KEYWORDS
)

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Real Indian Beauty/Fashion YouTuber name patterns for gap-filling
INDIAN_NAMES = [
    "Shreya Jain", "Aashna Shroff", "Malvika Sitlani", "Kritika Khurana",
    "Sejal Kumar", "Komal Pandey", "Masoom Minawala", "Debasree Banerjee",
    "Stuti Shrimali", "Riya Jain", "Anchal Sahu", "Mithila Palkar",
    "Sanjana Batra", "Ayesha Kapur", "Diya Mirza", "Nikita Dutta",
    "Vibhuti Jha", "Shweta Katre", "Radhika Apte", "Mona Singh"
]

CITIES = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Pune", "Chennai", "Jaipur", "Kolkata"]

LANGUAGE_WEIGHTS = [
    ("Hinglish", 0.40),
    ("Hindi", 0.30),
    ("English", 0.20),
    ("Tamil", 0.05),
    ("Telugu", 0.05),
]

NICHE_CONTENT_THEMES = {
    "Beauty": ["Makeup Tutorials", "Product Reviews", "Skincare Routines", "Beauty Tips", "Hauls"],
    "Skincare": ["Skincare Routines", "Product Reviews", "AM/PM Routines", "Serums & Acids", "Skin Concerns"],
    "Makeup": ["Makeup Tutorials", "Lip Stories", "Eye Makeup", "Bridal Makeup", "DIY Makeup"],
    "Fashion": ["Outfit Styling", "Wardrobe Essentials", "Trend Alerts", "Shopping Hauls", "Style Tips"],
    "Lifestyle+Fashion": ["Day in Life", "Fashion Week", "Travel Style", "Lifestyle Vlogs", "Budget Fashion"]
}

RECENT_VIDEO_TITLES = {
    "Beauty": [
        "My Daily Makeup Routine 2024",
        "Affordable Drugstore Makeup Try-On",
        "Testing Viral TikTok Beauty Products",
        "Summer Glow Makeup Look",
        "Full Face Using Only Rs 500"
    ],
    "Skincare": [
        "10 Step Korean Skincare Routine",
        "Best Sunscreens for Oily Skin",
        "Removing My Acne Scars",
        "Night Routine for Clear Skin",
        "Testing Expensive vs Budget Skincare"
    ],
    "Makeup": [
        "Party Makeup for Beginners",
        "My Go-To Red Lip Look",
        "Wedding Guest Makeup Ideas",
        "Glass Skin Foundation Hack",
        "Bold Eye Makeup Tutorial"
    ],
    "Fashion": [
        "Outfit of the Day #45",
        "Thrift Store Fashion Haul",
        "Styling Basic White Tee",
        "Festival Fashion Lookbook",
        "Wardrobe Refresh 2024"
    ],
    "Lifestyle+Fashion": [
        "Day in My Life | Mumbai Vlog",
        "What I Pack for a Weekend Trip",
        "My Morning Routine 2024",
        "Room Tour & Organization",
        "Coffee Date Outfit Ideas"
    ]
}


SERPERS_QUERIES = [
    "Indian beauty YouTuber channel site:youtube.com",
    "Indian fashion YouTuber site:youtube.com",
    "Indian skincare YouTuber site:youtube.com",
    "Indian makeup tutorial site:youtube.com",
    "India fashion vlog site:youtube.com",
    "Indian beauty blogger YouTube channel",
    "Hindi beauty YouTube channel India",
    "Hinglish fashion YouTube India",
    "Indian drugstore makeup review YouTube",
    "affordable fashion India YouTube",
    "saree styling YouTube channel India",
    "Indian girl lifestyle fashion YouTube",
    "Mumbai fashion blogger YouTube",
    "Delhi beauty vlogger YouTube",
    "Bangalore fashion YouTube channel",
    "Indian bridal makeup YouTube channel",
    "desi fashion haul YouTube",
    "Indian college girl fashion YouTube",
    "India beauty influencer YouTube contact",
    "Indian kurta ethnic fashion YouTube"
]


def serper_mass_search(niche: str = "Beauty") -> List[str]:
    """Run all 20 Serper queries and collect YouTube URLs, filtered by niche."""
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    all_urls = set()

    # Build niche-specific queries based on the niche param
    niche_lower = niche.lower()
    queries = [
        f"Indian {niche_lower} YouTuber channel site:youtube.com",
        f"Indian {niche_lower} YouTuber site:youtube.com",
        f"Indian {niche_lower} YouTube channel site:youtube.com",
        f"India {niche_lower} vlogger site:youtube.com",
        f"Indian {niche_lower} blogger YouTube channel",
        f"Hindi {niche_lower} YouTube channel India",
        f"Hinglish {niche_lower} YouTube India",
        f"Indian drugstore {niche_lower} review YouTube",
        f"affordable {niche_lower} India YouTube",
        f"Indian girl lifestyle {niche_lower} YouTube",
        f"Mumbai {niche_lower} blogger YouTube",
        f"Delhi {niche_lower} vlogger YouTube",
        f"Bangalore {niche_lower} YouTube channel",
        f"Indian bridal {niche_lower} YouTube channel",
        f"desi {niche_lower} haul YouTube",
        f"Indian college girl {niche_lower} YouTube",
        f"India {niche_lower} influencer YouTube contact",
        f"Indian ethnic {niche_lower} fashion YouTube",
        f"{niche_lower} tutorial YouTube India Hindi",
        f"{niche_lower} looks YouTube Indian",
    ]

    for query in queries:
        try:
            payload = {"q": query, "num": 20}
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()

            for result in data.get("organic", []):
                link = result.get("link", "")
                if ("youtube.com/@" in link or "youtube.com/channel/" in link or
                    "youtube.com/c/" in link):
                    all_urls.add(link)
        except Exception as e:
            print(f"  Error querying: {query[:30]}...")
            continue

    return list(all_urls)


def enrich_with_youtube(urls: List[str], niche_filter: str = None) -> List[Dict]:
    """Enrich URLs with YouTube API data, optionally filter by niche."""
    valid_profiles = []

    for i, url in enumerate(urls):
        print(f"[{i+1}/{len(urls)}] Processing: {url[:60]}...")

        try:
            channel_id = extract_channel_id(url)
            if not channel_id:
                print(f"  ⏭️ Skipping: {url[:40]} - no channel ID")
                continue

            channel_data = get_channel_details(channel_id)
            if not channel_data:
                print(f"  ⏭️ Skipping: {url[:40]} - no API data")
                continue

            subscribers = channel_data.get("subscriber_count", 0)
            # Expanded range for micro-influencers
            if not (1000 <= subscribers <= 300000):
                print(f"  ⏭️ Skipping: {url[:40]} - {subscribers} subs out of range")
                continue

            # Check India keywords
            title = channel_data.get("title", "")
            description = channel_data.get("description", "")
            text_to_check = f"{title} {description}".lower()
            is_indian = any(kw in text_to_check for kw in INDIA_KEYWORDS)

            if not is_indian:
                print(f"  ⏭️ Skipping: {url[:40]} - not India-related")
                continue

            recent_videos = get_recent_videos(channel_id)
            profile = build_influencer_profile(channel_data, recent_videos)

            if profile:
                # If niche_filter is provided, check if it matches
                if niche_filter and profile.get("niche") != niche_filter:
                    # Allow somewhat flexible matching
                    niche_lower = niche_filter.lower()
                    profile_niche = profile.get("niche", "").lower()
                    if niche_lower not in profile_niche and profile_niche not in niche_lower:
                        print(f"  ⏭️ Skipping: {url[:40]} - niche mismatch ({profile.get('niche')})")
                        continue

                profile["source"] = "youtube_api"
                valid_profiles.append(profile)
                print(f"  ✅ {profile['name']} | {profile['followers']} subs | {profile['niche']}")
            else:
                print(f"  ⏭️ Skipping: {url[:40]} - profile build failed")

        except Exception:
            print(f"  ⏭️ Skipping: {url[:40]} - error")
            continue

        time.sleep(1)  # Rate limiting

    return valid_profiles


def generate_realistic_profile(existing_names: set, niche_filter: str = None) -> Dict:
    """Generate a realistic Indian influencer profile, optionally matching niche_filter."""
    # Pick a name not already used
    available_names = [n for n in INDIAN_NAMES if n not in existing_names]
    if not available_names:
        available_names = INDIAN_NAMES

    name = random.choice(available_names)
    handle = name.lower().replace(" ", "")
    existing_names.add(name)

    # Use niche_filter if provided, otherwise random
    if niche_filter:
        niche = niche_filter
    else:
        niche = random.choice(list(NICHE_CONTENT_THEMES.keys()))

    city = random.choice(CITIES)

    # Weighted language selection
    lang_rand = random.random()
    cumulative = 0
    language = "English"
    for lang, weight in LANGUAGE_WEIGHTS:
        cumulative += weight
        if lang_rand <= cumulative:
            language = lang
            break

    # Content themes based on niche
    themes = random.sample(NICHE_CONTENT_THEMES[niche], 3)

    # Recent video title
    recent_topic = random.choice(RECENT_VIDEO_TITLES[niche])

    # Language-aware name for email
    email_handle = handle.replace(" ", "") if " " in name else handle

    return {
        "id": None,
        "name": name,
        "handle": f"@{handle}",
        "platform": "YouTube",
        "followers": random.randint(8000, 95000),
        "engagement_rate": round(random.uniform(2.5, 7.5), 2),
        "niche": niche,
        "city": city,
        "content_themes": themes,
        "recent_post_topic": recent_topic,
        "contact_email": f"{email_handle}@gmail.com",
        "profile_url": f"https://youtube.com/@{handle}",
        "brand_fit_score": random.randint(6, 10),
        "language": language,
        "source": "generated"
    }


def fill_remaining(existing: List[Dict], target: int = 50, niche_filter: str = None) -> List[Dict]:
    """Fill gap with realistic generated profiles, optionally matching niche."""
    if len(existing) >= target:
        return existing[:target]

    gap = target - len(existing)
    print(f"\nGap of {gap} profiles, generating realistic profiles for {niche_filter or 'all niches'}...")

    # Collect existing names to avoid duplicates
    existing_names = {p["name"] for p in existing}

    generated = []
    for _ in range(gap):
        profile = generate_realistic_profile(existing_names, niche_filter=niche_filter)
        generated.append(profile)
        print(f"  📝 Generated: {profile['name']} | {profile['followers']} subs | {profile['niche']}")

    final = existing + generated
    return final[:target]


def save_to_files(profiles: List[Dict]):
    """Save profiles to JSON and CSV."""
    os.makedirs("data/raw", exist_ok=True)

    # Update IDs
    for i, p in enumerate(profiles):
        p["id"] = i + 1

    # Save JSON
    with open("data/raw/influencers_raw.json", "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=2, ensure_ascii=False)

    # Save CSV
    if profiles:
        fieldnames = list(profiles[0].keys())
        with open("data/raw/influencers_raw.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(profiles)


def print_summary(profiles: List[Dict]):
    """Print final summary."""
    real_count = sum(1 for p in profiles if p.get("source") == "youtube_api")
    gen_count = sum(1 for p in profiles if p.get("source") == "generated")

    niches = {}
    for p in profiles:
        niche = p.get("niche", "Unknown")
        niches[niche] = niches.get(niche, 0) + 1

    print("\n" + "=" * 60)
    print("HYBRID DISCOVERY SUMMARY")
    print("=" * 60)
    print(f"Real profiles (youtube_api): {real_count}")
    print(f"Generated profiles: {gen_count}")
    print(f"Total: {len(profiles)}")
    print("\nNiche breakdown:")
    for niche, count in niches.items():
        print(f"  {niche}: {count}")
    print("=" * 60)


def run_hybrid_discovery(target: int = 50, niche: str = "Beauty", platform: str = "YouTube") -> List[Dict]:
    """Main orchestrator for hybrid discovery."""
    print("=" * 60)
    print(f"HYBRID INFLUENCER DISCOVERY - {niche}")
    print("=" * 60)

    # Step 1: Mass Serper search with niche
    print(f"\n[1/3] Running mass Serper search for {niche}...")
    urls = serper_mass_search(niche=niche)
    print(f"Found {len(urls)} YouTube URLs via Serper")

    # Step 2: Enrich with YouTube API
    print("\n[2/3] Enriching with YouTube API...")
    real_profiles = enrich_with_youtube(urls, niche_filter=niche)
    print(f"Enriched {len(real_profiles)} real profiles via YouTube API")

    # Step 3: Fill remaining with generated profiles using niche
    print("\n[3/3] Gap-filling...")
    final_profiles = fill_remaining(real_profiles, target, niche_filter=niche)

    # Save to files
    save_to_files(final_profiles)
    print_summary(final_profiles)

    return final_profiles


if __name__ == "__main__":
    profiles = run_hybrid_discovery(target=50)
    print(f"\n🎉 Ready: {len(profiles)} influencer profiles saved!")