"""
Environment variable loader for Termii API settings.
Loads environment variables from a .env file and sets up Termii API configuration.
"""

import os
from dotenv import load_dotenv

load_dotenv()

TERMII_API_KEY: str = os.getenv("TERMII_API_KEY")
TERMII_BASE_URL: str = os.getenv("TERMII_BASE_URL")