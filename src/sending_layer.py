"""Outreach execution explanation and mock API flow."""
import pandas as pd
import json
import os
from datetime import datetime


def explain_email_sending_workflow() -> dict:
    """Returns a dict explaining the email sending workflow."""
    return {
        "method": "SMTP via Gmail API or SendGrid API",
        "api_used": "SendGrid API v3 / Gmail SMTP",
        "endpoint": "https://api.sendgrid.com/v3/mail/send",
        "auth": "Bearer API Key in Authorization header",
        "rate_limit": "100 emails/day (free tier), 40,000/month (paid)",
        "steps": [
            "1. Load enriched influencer data with generated email pitches",
            "2. Filter by outreach_priority = High or Medium",
            "3. For each influencer, construct email payload with to, subject, body",
            "4. POST to SendGrid API endpoint with auth header",
            "5. Log response status (202 = success)",
            "6. Store sent status + timestamp in outputs/sent_log.csv"
        ],
        "payload_example": {
            "to": "influencer@gmail.com",
            "subject": "Collaboration Opportunity with Conversely AI Private Limited",
            "body": "<generated email pitch>",
            "from": "outreach@converselyai.com"
        }
    }


def explain_dm_sending_workflow() -> dict:
    """Returns a dict explaining Instagram DM workflow."""
    return {
        "method": "Instagram Graph API - Send Message",
        "api_used": "Meta Graph API v18.0",
        "endpoint": "https://graph.facebook.com/v18.0/me/messages",
        "auth": "Page Access Token via Meta Developer App",
        "prerequisites": [
            "Instagram Business/Creator account required",
            "Meta Developer App with instagram_manage_messages permission",
            "Influencer must have messaged the brand page first (due to Meta policy)"
        ],
        "steps": [
            "1. Authenticate via Meta OAuth and get Page Access Token",
            "2. Load DM pitches from outputs/messages/outreach_messages.json",
            "3. For each influencer, find their Instagram user ID via IG username search",
            "4. POST message payload to Graph API messages endpoint",
            "5. Handle rate limits: max 1000 messages/day per account",
            "6. Log delivery status in outputs/sent_log.csv"
        ],
        "payload_example": {
            "recipient": {"id": "<instagram_user_id>"},
            "message": {"text": "<generated DM pitch>"}
        },
        "limitation": "Cold DMs require influencer to initiate contact first per Meta policy"
    }


def mock_send_email(influencer_message: dict) -> dict:
    """Simulates sending an email (no real API call)."""
    print(f"📧 Sending email to {influencer_message['name']} at {influencer_message['email']}...")
    return {
        "id": influencer_message["id"],
        "name": influencer_message["name"],
        "email": influencer_message["email"],
        "channel": "email",
        "status": "sent (mock)",
        "timestamp": datetime.now().isoformat()
    }


def mock_send_dm(influencer_message: dict) -> dict:
    """Simulates sending an Instagram DM."""
    print(f"📱 Sending DM to {influencer_message['handle']}...")
    return {
        "id": influencer_message["id"],
        "name": influencer_message["name"],
        "handle": influencer_message["handle"],
        "channel": "instagram_dm",
        "status": "sent (mock)",
        "timestamp": datetime.now().isoformat()
    }


def run_mock_sending_campaign(messages: list) -> pd.DataFrame:
    """Runs mock sending campaign and returns log DataFrame."""
    results = []

    for msg in messages:
        email_result = mock_send_email(msg)
        results.append(email_result)

        dm_result = mock_send_dm(msg)
        results.append(dm_result)

    log_df = pd.DataFrame(results)

    os.makedirs("outputs/sent_log", exist_ok=True)
    log_df.to_csv("outputs/sent_log/sent_log.csv", index=False)

    emails_sent = len(log_df[log_df["channel"] == "email"])
    dms_sent = len(log_df[log_df["channel"] == "instagram_dm"])

    print(f"Campaign complete: {emails_sent} emails sent, {dms_sent} DMs sent")

    return log_df


if __name__ == "__main__":
    import json

    with open("outputs/messages/outreach_messages.json") as f:
        messages = json.load(f)

    email_wf = explain_email_sending_workflow()
    dm_wf = explain_dm_sending_workflow()

    print("\n=== EMAIL WORKFLOW ===")
    print(json.dumps(email_wf, indent=2))

    print("\n=== DM WORKFLOW ===")
    print(json.dumps(dm_wf, indent=2))

    log_df = run_mock_sending_campaign(messages[:3])
    print(log_df)