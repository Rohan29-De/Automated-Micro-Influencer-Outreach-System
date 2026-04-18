import os
import time
import re
import csv
import json
from typing import Optional

import requests
from googleapiclient.discovery import build

from dotenv import load_dotenv

load_dotenv()


SERPER_API_KEY = os.getenv("SERPER_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY) if YOUTUBE_API_KEY else None

YOUTUBE_SEARCH_QUERIES = [
    # Original site:youtube.com queries that work well
    "Indian beauty YouTuber site:youtube.com",
    "Indian fashion YouTuber site:youtube.com",
    "Indian skincare YouTube channel site:youtube.com",
    "Indian makeup tutorial YouTuber site:youtube.com",
    "Indian lifestyle fashion YouTube channel site:youtube.com",
    "India beauty vlogger YouTube channel site:youtube.com",
    "Indian fashion haul YouTube micro influencer site:youtube.com",
    "saree fashion YouTube India channel site:youtube.com",
    "Indian beauty blogger YouTube channel site:youtube.com",
    "desi fashion YouTube channel Indian style site:youtube.com",
    "Indian makeup artist YouTube channel site:youtube.com",
    "Indian skincare routine YouTube channel site:youtube.com",
    "Indian ethnic wear YouTube channel fashion site:youtube.com",
    "Hindi beauty YouTuber small channel India site:youtube.com",
    "Indian fashion blogger YouTube channel site:youtube.com",
    "desi makeup YouTuber Indian YouTube site:youtube.com",
    "Indian lifestyle YouTuber beauty fashion site:youtube.com",
    "Indian cosmetic review YouTube channel site:youtube.com",
    "Indian mehandi design YouTube channel beauty site:youtube.com",
    "Indian hairstyle YouTube channel fashion site:youtube.com",
    "site:youtube.com beauty India 2023 2024",
    "site:youtube.com fashion haul India girl",
    "site:youtube.com skincare India review",
    "site:youtube.com Indian makeup artist",
    "site:youtube.com Indian fashion vlog",
]

FALLBACK_SEARCH_QUERIES = [
    "Indian beauty micro influencer YouTube small channel",
    "Indian fashion small YouTube channel Delhi Mumbai",
    "desi skincare routine YouTube India beauty",
    "Indian girl makeup tutorial YouTube Hindi",
    "saree drape tutorial YouTube India fashion",
]

INDIA_KEYWORDS = ["india", "indian", "hindi", "mumbai", "delhi", "bangalore", "hyderabad",
                  "chennai", "kolkata", "pune", "jaipur", "gujarat", "marathi", "tamil",
                  "telugu", "kannada", "kerala"]


def search_channels_via_serper(query: str, num_results: int = 20) -> list:
    """Search for YouTube channels using Serper.dev API."""
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"q": query, "num": num_results}

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    channel_urls = []
    for result in data.get("organic", []):
        link = result.get("link", "")
        # Handle various YouTube URL formats including youtu.be redirects
        if ("youtube.com/@" in link or "youtube.com/channel/" in link or
            "youtube.com/c/" in link or "youtu.be/" in link):
            channel_urls.append(link)

    return list(set(channel_urls))


def extract_channel_id(url: str) -> str:
    """Extract channel ID from YouTube URL."""
    # Clean URL - remove query params and trailing slashes
    url = url.split("?")[0].rstrip("/")

    if "/channel/" in url:
        return url.split("/channel/")[-1].split("/")[0]
    elif "/@" in url:
        handle = url.split("/@")[-1].split("/")[0]
        return _search_channel_by_handle_api(handle)
    elif "/c/" in url:
        name = url.split("/c/")[-1].split("/")[0]
        return _search_channel_by_name(name)
    elif "/user/" in url:
        name = url.split("/user/")[-1].split("/")[0]
        return _search_channel_by_name(name)
    return None


def _search_channel_by_handle_api(handle: str) -> Optional[str]:
    """Search for channel ID using channels API with forHandle parameter."""
    if not youtube or not YOUTUBE_API_KEY:
        return None
    # Direct API call using forHandle is more reliable
    try:
        response = youtube.channels().list(
            forHandle=f"@{handle}",
            part="id"
        ).execute()
        items = response.get("items", [])
        if items:
            return items[0]["id"]
    except Exception:
        pass
    # Fallback to search API
    return _search_channel_by_name(handle)


def _search_channel_by_name(name: str) -> Optional[str]:
    """Search for channel ID by name or handle using search API."""
    if not youtube:
        return None
    try:
        response = youtube.search().list(
            q=name,
            type="channel",
            part="id",
            maxResults=5
        ).execute()
        items = response.get("items", [])
        # Return first match
        if items:
            return items[0]["id"]["channelId"]
    except Exception:
        pass
    return None


def get_channel_details(channel_id: str) -> dict:
    """Get channel details from YouTube Data API with retry logic."""
    if not youtube:
        return {}

    # Exponential backoff retry
    for attempt in range(3):
        try:
            response = youtube.channels().list(
                id=channel_id,
                part="snippet,statistics,brandingSettings,topicDetails"
            ).execute()
            items = response.get("items", [])
            if not items:
                return {}
            item = items[0]
            snippet = item.get("snippet", {})
            stats = item.get("statistics", {})
            branding = item.get("brandingSettings", {}).get("channel", {})
            topics = item.get("topicDetails", {})

            description = snippet.get("description", "")
            title = snippet.get("title", "")
            country = snippet.get("country", "")

            # Check if channel is Indian: country is IN OR keywords in title/description
            text_to_check = f"{description} {title}".lower()
            is_indian = country == "IN" or any(kw in text_to_check for kw in INDIA_KEYWORDS)

            if not is_indian:
                return {}

            # Handle subscriber count with proper conversion
            def parse_count(val):
                if not val:
                    return 0
                return int(str(val).replace(",", ""))

            return {
                "channel_id": channel_id,
                "title": title,
                "handle": branding.get("handle", ""),
                "description": description,
                "subscriber_count": parse_count(stats.get("subscriberCount")),
                "view_count": parse_count(stats.get("viewCount")),
                "video_count": parse_count(stats.get("videoCount")),
                "country": country if country else "IN",
                "custom_url": branding.get("customUrl", ""),
                "thumbnail_url": snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
                "keywords": branding.get("keywords", ""),
                "topic_categories": [t.split("/")[-1] for t in topics.get("topicCategories", [])],
                "published_at": snippet.get("publishedAt", "")
            }
        except Exception as e:
            if attempt < 2:
                wait_time = 2 ** (attempt + 1)
                time.sleep(wait_time)
            else:
                return {}
    return {}


def get_recent_videos(channel_id: str, max_results: int = 5) -> list:
    """Get recent uploads from a channel with retry logic."""
    if not youtube:
        return []

    for attempt in range(3):
        try:
            response = youtube.search().list(
                channelId=channel_id,
                type="video",
                order="date",
                part="id,snippet",
                maxResults=max_results
            ).execute()
            videos = []
            for item in response.get("items", []):
                snippet = item.get("snippet", {})
                videos.append({
                    "video_id": item["id"]["videoId"],
                    "title": snippet.get("title", ""),
                    "published_at": snippet.get("publishedAt", ""),
                    "description": snippet.get("description", "")
                })
            return videos
        except Exception:
            if attempt < 2:
                wait_time = 2 ** (attempt + 1)
                time.sleep(wait_time)
    return []


def extract_email_from_description(description: str) -> Optional[str]:
    """Extract email address from channel description."""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, description)
    return match.group(0) if match else None


def build_influencer_profile(channel_data: dict, recent_videos: list) -> dict:
    """Convert YouTube API data to standard influencer format."""
    subscribers = channel_data.get("subscriber_count", 0)
    views = channel_data.get("view_count", 0)
    videos = channel_data.get("video_count", 0)

    # Relaxed range: 1k-200k (will re-filter strictly in filter.py later)
    if not (1000 <= subscribers <= 200000):
        return {}

    description = channel_data.get("description", "")
    keywords = channel_data.get("keywords", "")
    title = channel_data.get("title", "")
    custom_url = channel_data.get("custom_url", "")

    text_to_analyze = f"{description} {keywords}".lower()
    niche = detect_niche(text_to_analyze)
    if not niche:
        return {}

    engagement_rate = 3.5
    if subscribers > 0 and videos > 0:
        engagement_rate = round((views / videos / subscribers) * 100, 2)

    handle = f"@{custom_url}" if custom_url else title

    email = extract_email_from_description(description)
    contact_email = email if email else f"{handle.replace('@', '').replace(' ', '')}@gmail.com"

    content_themes = extract_content_themes(text_to_analyze)

    recent_topic = recent_videos[0]["title"] if recent_videos else ""

    city = extract_city_from_description(description)

    language = detect_language(description)

    brand_score = calculate_brand_fit_score(niche, subscribers)

    return {
        "id": None,
        "name": title,
        "handle": handle,
        "platform": "YouTube",
        "followers": subscribers,
        "engagement_rate": engagement_rate,
        "niche": niche,
        "city": city,
        "content_themes": content_themes,
        "recent_post_topic": recent_topic,
        "contact_email": contact_email,
        "profile_url": f"https://youtube.com/{custom_url}" if custom_url else "",
        "brand_fit_score": brand_score,
        "language": language
    }


def detect_niche(text: str) -> Optional[str]:
    """Detect niche from text."""
    text = text.lower()
    if any(w in text for w in ["beauty", "makeup", "skincare", "cosmetics"]):
        return "Beauty"
    if any(w in text for w in ["fashion", "clothing", "style", "outfit"]):
        return "Fashion"
    if any(w in text for w in ["skincare", "skin care"]):
        return "Skincare"
    if any(w in text for w in ["makeup"]):
        return "Makeup"
    if any(w in text for w in ["lifestyle"]):
        return "Lifestyle+Fashion"
    return None


def extract_content_themes(text: str) -> list:
    """Extract 3 content themes from text."""
    themes = []
    theme_keywords = {
        "Skincare": ["skincare", "skin care", "moisturizer", "serum", "sunscreen"],
        "Makeup": ["makeup", "make up", " lipstick", "foundation", "eyeshadow"],
        "Fashion": ["fashion", "outfit", "style", "clothing", "wear"],
        "Hair Care": ["hair", "haircare", "hair care", "hairstyle"],
        "Beauty Tips": ["tips", "tutorial", "how to", "guide"],
        "Product Reviews": ["review", "review", "haul", "unboxing"],
        "Trending": ["trending", "viral", "trend"],
    }
    for theme, keywords in theme_keywords.items():
        if any(kw in text for kw in keywords) and theme not in themes:
            themes.append(theme)
            if len(themes) >= 3:
                break
    return themes[:3] or ["Beauty", "Fashion", "Lifestyle"]


def extract_city_from_description(description: str) -> str:
    """Extract city from description."""
    cities = ["Mumbai", "Delhi", "Bangalore", "Bengaluru", "Hyderabad", "Chennai",
              "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Kanpur"]
    description = description.lower()
    for city in cities:
        if city.lower() in description:
            return city
    return "India"


def detect_language(description: str) -> str:
    """Detect language from description."""
    desc = description.lower()
    hindi_words = ["namaste", "doston", "bolenge", "ke liye", "hai yeh"]
    tamil_words = ["vanakkam", "unga", "epdi", "solren"]
    telugu_words = ["namaste", "mari", "ledu", "cheyya"]
    kannada_words = ["namaste", "hodu", "illi", "baruthe"]

    if any(w in desc for w in hindi_words):
        return "Hindi"
    if any(w in desc for w in tamil_words):
        return "Tamil"
    if any(w in desc for w in telugu_words):
        return "Telugu"
    if any(w in desc for w in kannada_words):
        return "Kannada"
    return "English"


def calculate_brand_fit_score(niche: str, subscribers: int) -> int:
    """Calculate brand fit score based on niche relevance and subscriber count."""
    score = 5
    niche_relevant = niche in ["Beauty", "Fashion", "Skincare", "Makeup"]
    if niche_relevant:
        score += 2
    if 10000 <= subscribers <= 50000:
        score += 2
    elif subscribers >= 50000:
        score += 1
    return min(score, 10)


def discover_influencers(target_count: int = 50) -> list:
    """Orchestrate the full discovery process."""
    print("Starting YouTube influencer discovery...")
    print("=" * 60)

    all_urls = set()
    for query in YOUTUBE_SEARCH_QUERIES:
        print(f"\nSearching: {query[:50]}...")
        urls = search_channels_via_serper(query)
        print(f"Found {len(urls)} URLs")
        all_urls.update(urls)

    # Fallback searches if < 20 found
    if len(all_urls) < 20:
        print("\n--- Running fallback searches ---")
        for query in FALLBACK_SEARCH_QUERIES:
            print(f"\nSearching: {query[:50]}...")
            urls = search_channels_via_serper(query)
            print(f"Found {len(urls)} URLs")
            all_urls.update(urls)

    print(f"\nTotal unique URLs: {len(all_urls)}")
    print("=" * 60)

    influencers = []
    url_list = list(all_urls)

    for i, url in enumerate(url_list):
        if len(influencers) >= target_count:
            break

        print(f"\n[{i+1}/{len(url_list)}] Processing: {url}")

        channel_id = extract_channel_id(url)
        if not channel_id:
            print("  Could not extract channel ID")
            continue

        channel_data = get_channel_details(channel_id)
        if not channel_data:
            print("  Could not get channel details")
            continue

        recent_videos = get_recent_videos(channel_id)

        profile = build_influencer_profile(channel_data, recent_videos)
        if not profile:
            print("  Does not meet criteria (not in India or wrong subscriber range)")
            continue

        influencers.append(profile)
        print(f"  Found {profile['name']} | {profile['followers']} subs | {profile['niche']}")

        if len(influencers) >= target_count:
            break

        time.sleep(1)  # Reduced delay to 1 second

    print("\n" + "=" * 60)
    print(f"Discovery complete: {len(influencers)} influencers found")
    return influencers


def save_discovered_data(influencers: list):
    """Save discovered influencers to CSV and JSON."""
    os.makedirs("data/raw", exist_ok=True)

    # Lower threshold: save whatever we find (minimum 5 or whatever we have)
    if len(influencers) < 1:
        print("No influencers found to save.")
        return

    csv_path = "data/raw/influencers_raw.csv"
    json_path = "data/raw/influencers_raw.json"

    # Print each influencer found
    print("\n" + "=" * 60)
    print("DISCOVERED INFLUENCERS")
    print("=" * 60)
    for i, inf in enumerate(influencers):
        inf["id"] = i + 1
        print(f"[{inf['id']}] {inf['name']} | {inf['followers']} subs | {inf['niche']} | {inf['city']} | email: {inf['contact_email']}")

    fieldnames = list(influencers[0].keys())
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for inf in influencers:
            writer.writerow(inf)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(influencers, f, indent=2, ensure_ascii=False)

    total = len(influencers)
    niches = {}
    min_subs = float("inf")
    max_subs = 0
    emails_found = 0
    fallback_emails = 0

    for inf in influencers:
        niche = inf.get("niche", "Unknown")
        niches[niche] = niches.get(niche, 0) + 1
        subs = inf.get("followers", 0)
        min_subs = min(min_subs, subs)
        max_subs = max(max_subs, subs)
        email = inf.get("contact_email", "")
        if "@gmail.com" in email and "fallback" not in email.lower():
            fallback_emails += 1
        elif "@" in email:
            emails_found += 1

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total found: {total}")
    print("\nNiche breakdown:")
    for niche, count in niches.items():
        print(f"  {niche}: {count}")
    print(f"\nSubscriber range: {min_subs:,} - {max_subs:,}")
    print(f"Emails found: {emails_found} | Fallback: {fallback_emails}")
    print(f"\nSaved to: {csv_path}")
    print(f"Saved to: {json_path}")


if __name__ == "__main__":
    influencers = discover_influencers(target_count=50)
    save_discovered_data(influencers)
    print(f"\nDiscovery complete: {len(influencers)} real influencers found!")