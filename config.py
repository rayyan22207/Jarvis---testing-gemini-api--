# config.py
import os
import sys
from dotenv import load_dotenv

# --- Silence gRPC/absl noise BEFORE importing google.generativeai ---
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "3"

# Log all stderr (warnings/errors) to a file instead of console
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
_log_path = os.path.join(LOG_DIR, "gemini_logs.txt")
# Line-buffered text file so entries flush frequently
sys.stderr = open(_log_path, mode="a", encoding="utf-8", buffering=1)

import google.generativeai as genai  # noqa: E402  (import after env tweaks)

# Load .env and configure API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env")

genai.configure(api_key=API_KEY)

# Default model for your helpers
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

def get_model(name: str | None = None) -> "genai.GenerativeModel":
    """Return a configured GenerativeModel (defaults to fast/free-tier friendly)."""
    return genai.GenerativeModel(name or DEFAULT_MODEL)
