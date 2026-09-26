import os
from pathlib import Path

from dotenv import load_dotenv


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
PANELS_DIR = STATIC_DIR / "panels"
EXPORTS_DIR = STATIC_DIR / "exports"


# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------

load_dotenv(BASE_DIR / ".env")


# ---------------------------------------------------------
# Application settings
# ---------------------------------------------------------

APP_NAME = os.getenv("APP_NAME", "ComicCraft")

DEBUG = os.getenv("DEBUG", "true").lower() == "true"


# ---------------------------------------------------------
# Gemini configuration
# ---------------------------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

GEMINI_OUTLINE_MODEL = os.getenv(
    "GEMINI_OUTLINE_MODEL",
    "gemini-1.5-flash",
)

GEMINI_STORY_MODEL = os.getenv(
    "GEMINI_STORY_MODEL",
    "gemini-1.5-pro",
)


# ---------------------------------------------------------
# Image configuration
# ---------------------------------------------------------

IMAGE_PROVIDER = os.getenv(
    "IMAGE_PROVIDER",
    "mock",
).lower()

HF_API_KEY = os.getenv(
    "HF_API_KEY",
    "",
).strip()

HF_IMAGE_MODEL = os.getenv(
    "HF_IMAGE_MODEL",
    "stabilityai/stable-diffusion-xl-base-1.0",
)

LOCAL_IMAGE_MODEL = os.getenv(
    "LOCAL_IMAGE_MODEL",
    "runwayml/stable-diffusion-v1-5",
)


# ---------------------------------------------------------
# Comic configuration
# ---------------------------------------------------------

try:
    PANEL_COUNT = int(
        os.getenv("PANEL_COUNT", "5")
    )
except ValueError:
    PANEL_COUNT = 5


# ---------------------------------------------------------
# Directory creation
# ---------------------------------------------------------

PANELS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

EXPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
    )