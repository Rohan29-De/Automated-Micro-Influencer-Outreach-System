"""Message generation using Groq API."""
import os
import time
import pandas as pd
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def get_groq_client():
    """Returns a Groq client instance using llama-3.1-8b-instant model."""
    api_key = os.getenv("GROQ_API_KEY")
    return Groq(api_key=api_key)


def generate_email_pitch(influencer: dict) -> str:
    """Generates a professional collaboration email using Groq API."""
    client = get_groq_client()

    system_prompt = (
        "You are an outreach specialist for Conversely AI Private Limited, "
        "a brand in the Beauty/Fashion space. Write professional, warm, and "
        "personalized collaboration emails."
    )

    user_prompt = f"""Write a collaboration email pitch for:

- Influencer Name: {influencer['name']}
- Handle: {influencer['handle']}
- Niche: {influencer['niche']}
- City: {influencer['city']}
- Content Themes: {influencer.get('content_theme_summary', influencer.get('content_themes', []))}
- Recent Post Topic: {influencer['recent_post_topic']}
- Platform: {influencer['platform']}
- Engagement Rate: {influencer['engagement_rate']}%
- Tier: {influencer.get('tier', 'Unknown')}
- Collaboration Type: Paid Sponsorship

Write a collaboration email pitch of 60-90 words. Reference their niche, content style, and recent post. End with a clear CTA. Do not use placeholders like [X] or [Y] - use actual details."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=200
    )

    return response.choices[0].message.content


def generate_dm_pitch(influencer: dict) -> str:
    """Generates a short Instagram DM pitch using Groq API."""
    client = get_groq_client()

    system_prompt = (
        "You are an outreach specialist for Conversely AI Private Limited, "
        "a brand in the Beauty/Fashion space."
    )

    user_prompt = f"""Write an Instagram DM for {influencer['name']} (@{influencer['handle']}) who creates {influencer['niche']} content in {influencer['city']}.

Write an Instagram DM of 15-30 words only. Friendly, casual tone. Mention their niche and a paid sponsorship opportunity with Conversely AI Private Limited. Do not use placeholders."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=100
    )

    return response.choices[0].message.content


def generate_messages_for_influencer(influencer: dict) -> dict:
    """Generates both email and DM pitches for a single influencer."""
    email_pitch = generate_email_pitch(influencer)
    time.sleep(1)  # Rate limit avoidance
    dm_pitch = generate_dm_pitch(influencer)

    return {
        "id": influencer["id"],
        "name": influencer["name"],
        "handle": influencer["handle"],
        "email": influencer["contact_email"],
        "email_pitch": email_pitch,
        "dm_pitch": dm_pitch,
        "outreach_priority": influencer.get("outreach_priority", "Medium")
    }


def generate_all_messages(enriched_df, priority_filter="High") -> list:
    """Generates messages for all influencers matching the priority filter."""
    filtered_df = enriched_df[enriched_df["outreach_priority"] == priority_filter]
    total = len(filtered_df)

    messages = []
    for idx, (_, row) in enumerate(filtered_df.iterrows(), 1):
        influencer = row.to_dict()
        print(f"Generating messages for {influencer['name']}... ({idx}/{total})")
        msg = generate_messages_for_influencer(influencer)
        messages.append(msg)

    return messages


def save_messages(messages: list):
    """Saves messages to JSON and CSV files."""
    os.makedirs("outputs/messages", exist_ok=True)

    json_path = "outputs/messages/outreach_messages.json"
    csv_path = "outputs/messages/outreach_messages.csv"

    with open(json_path, "w") as f:
        json.dump(messages, f, indent=2)

    # Flatten for CSV
    df = pd.DataFrame(messages)
    df.to_csv(csv_path, index=False)

    print(f"Saved {len(messages)} messages to outputs/messages/")


if __name__ == "__main__":
    import pandas as pd
    from dotenv import load_dotenv

    load_dotenv()
    df = pd.read_csv("data/enriched/influencers_enriched.csv")
    messages = generate_all_messages(df, priority_filter="High")
    save_messages(messages)