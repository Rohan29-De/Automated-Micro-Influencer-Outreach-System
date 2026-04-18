"""Configuration for backend - loads .env variables."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
project_root = Path(__file__).parent.parent.parent
env_path = project_root / ".env"
load_dotenv(env_path)

# API Keys
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# App settings
APP_NAME = "Micro-Influencer Outreach System"
DEBUG = os.getenv("DEBUG", "false").lower() == "true"