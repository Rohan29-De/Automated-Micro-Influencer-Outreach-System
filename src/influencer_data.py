"""50 influencer records."""
import random

INDIAN_FIRST_NAMES_FEMALE = [
    "Aisha", "Ananya", "Anika", "Avani", "Diya", "Ira", "Isha", "Kavya", "Kiara", "Lavanya",
    "Mahika", "Meera", "Myra", "Nisha", "Pari", "Priya", "Riya", "Saanvi", "Sakshi", "Sara",
    "Shreya", "Siya", "Sneha", "Tanisha", "Tara", "Vanshika", "Zoya", "Aditi", "Akriti", "Amrita"
]

INDIAN_FIRST_NAMES_MALE = [
    "Aditya", "Arjun", "Arnav", "Dev", "Dhruv", "Ishaan", "Kabir", "Karan", "Karthik", "Krishna",
    "Mayank", "Nikhil", "Princeton", "Rohan", "Sahil", "Samarth", "Siddharth", "Tanmay", "Vihaan", "Vikram"
]

INDIAN_LAST_NAMES = [
    "Sharma", "Patel", "Singh", "Verma", "Gupta", "Kumar", "Joshi", "Shah", "Mehta", "Reddy",
    "Rao", "Kapoor", "Malhotra", "Khanna", "Bhatia", "Chopra", "Dua", "Sinha", "Mishra", "Chatterjee"
]

CITIES = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Pune", "Chennai", "Kolkata", "Jaipur"]

NICHES = ["Beauty", "Fashion", "Skincare", "Makeup", "Lifestyle+Fashion"]

PLATFORMS = {
    "Instagram": 20,
    "YouTube": 10,
    "Instagram+YouTube": 20
}

LANGUAGE_PREFERENCES = {
    "Instagram": ["English", "Hinglish", "Hindi"],
    "YouTube": ["English", "Hinglish", "Hindi", "Tamil", "Telugu", "Kannada"],
    "Instagram+YouTube": ["English", "Hinglish", "Hindi", "Tamil", "Telugu", "Kannada"]
}

CONTENT_THEMES = {
    "Beauty": ["GRWM", "Product reviews", "Beauty tips", "Self-care routines", "Skinimalism", "Budget beauty", "Dupes & steals"],
    "Fashion": ["Outfit of the day", "Trend edits", "Budget fashion hauls", "Saree draping", "Ethnic wear", "Street style", "Wardrobe essentials"],
    "Skincare": ["Skincare routines", "10-step routine", "Acne solutions", "Sunscreen importance", "Vitamin C serums", "K-beauty secrets", "Dermatologist tips"],
    "Makeup": ["Makeup tutorials", "Festive looks", "Date night makeup", "Glazed lips", "Cut crease", "Brow shaping", "Contouring hacks"],
    "Lifestyle+Fashion": ["Day in my life", "Travel style", "Food diaries", "Fitness routines", "Home decor", "Workout looks", "Weekend outfits"]
}

RECENT_POST_TOPICS = {
    "Beauty": [
        "New serum that changed my skin",
        "Under-eye circles? Here's what works",
        "My holy grail skincare products",
        "Drugstore vs Luxury - you decide",
        "Summer skincare routine 2025"
    ],
    "Fashion": [
        "Outfit under 2000 rupees",
        "What I wore to a wedding",
        "Thrifted finds that look expensive",
        "Basic wardrobe essentials",
        "Festival outfit ideas"
    ],
    "Skincare": [
        "AM vs PM skincare routine",
        "Skin barrier repair tips",
        "Products that actually work for acne",
        "My nighttime routine",
        "Sunscreen reapplication tips"
    ],
    "Makeup": [
        "Easy 5-minute makeup look",
        "Lip liner trick you need to know",
        "Festival-ready makeup",
        "No-makeup makeup look",
        "Products for oily skin"
    ],
    "Lifestyle+Fashion": [
        "A day in my life as an influencer",
        "What I ate this week",
        "Morning routine that changed everything",
        "My travel capsule wardrobe",
        "Weekend outfit inspo"
    ]
}

EMAIL_DOMAINS = ["gmail.com", "outlook.com", "yahoo.com", "hotmail.com"]

random.seed(42)

def get_influencers():
    influencers = []
    names_used = set()

    def generate_name():
        while True:
            first = random.choice(INDIAN_FIRST_NAMES_FEMALE + INDIAN_FIRST_NAMES_MALE)
            last = random.choice(INDIAN_LAST_NAMES)
            full_name = f"{first} {last}"
            if full_name not in names_used:
                names_used.add(full_name)
                return full_name, first.lower(), last.lower()

    platform_list = []
    for platform, count in PLATFORMS.items():
        platform_list.extend([platform] * count)
    random.shuffle(platform_list)

    for i in range(1, 51):
        name, first_lower, last_lower = generate_name()
        platform = platform_list[i - 1]
        handle = f"{first_lower}{last_lower}{random.randint(1, 99)}"
        name_for_email = handle if random.random() > 0.3 else f"{first_lower}.{last_lower}"
        email_domain = random.choice(EMAIL_DOMAINS)
        contact_email = f"{name_for_email}@{email_domain}"

        followers = random.randint(5000, 100000)
        engagement_rate = round(random.uniform(1.5, 8.5), 2)
        niche = random.choice(NICHES)

        themes = random.sample(CONTENT_THEMES[niche], 3)
        recent_post_topic = random.choice(RECENT_POST_TOPICS[niche])
        city = random.choice(CITIES)
        language = random.choice(LANGUAGE_PREFERENCES[platform])

        if platform == "Instagram":
            profile_url = f"https://instagram.com/{handle}"
        elif platform == "YouTube":
            channel_name = f"{first_lower}{last_lower}{random.randint(1, 9)}beauty"
            profile_url = f"https://youtube.com/@{channel_name}"
        else:
            handle_ig = f"{handle}"
            channel_name = f"{first_lower}{last_lower}{random.randint(1, 9)}"
            profile_url = f"https://instagram.com/{handle_ig}"

        brand_fit_score = random.randint(6, 10)

        influencers.append({
            "id": i,
            "name": name,
            "handle": f"@{handle}",
            "platform": platform,
            "followers": followers,
            "engagement_rate": engagement_rate,
            "niche": niche,
            "city": city,
            "content_themes": themes,
            "recent_post_topic": recent_post_topic,
            "contact_email": contact_email,
            "profile_url": profile_url,
            "brand_fit_score": brand_fit_score,
            "language": language
        })

    return influencers


def save_raw_data():
    import pandas as pd
    import json
    import os

    influencers = get_influencers()
    df = pd.DataFrame(influencers)
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/influencers_raw.csv", index=False)
    with open("data/raw/influencers_raw.json", "w") as f:
        json.dump(influencers, f, indent=2)
    print(f"Saved {len(influencers)} influencers to data/raw/")
    return df