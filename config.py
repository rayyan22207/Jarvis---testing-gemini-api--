import os
from dotenv import load_dotenv
import sys

# Quiet gRPC + absl logging
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "3"

# Redirect stderr to a file (so warnings/errors go there, not your console)
sys.stderr = open("gemini_logs.txt", "w")

import google.generativeai as genai

# Load env vars
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env")

# Configure Gemini once here
genai.configure(api_key=API_KEY)
