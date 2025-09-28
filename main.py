import os
from dotenv import load_dotenv

# Quiet gRPC noise (optional)
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "3"

import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Put GEMINI_API_KEY in .env")

genai.configure(api_key=api_key)

def print_section(title):
    print("\n" + "=" * 8, title, "=" * 8)

# 1) List models you actually have
print_section("MODELS")
for m in genai.list_models():
    # show only text/multimodal chat models
    if "generateContent" in m.supported_generation_methods:
        print(m.name)

# 2) Basic text
print_section("BASIC TEXT")
model = genai.GenerativeModel("gemini-2.5-flash")
r = model.generate_content("Give me 3 bullets on why Django Channels is useful.")
print(r.text)

# 3) Streaming
print_section("STREAMING")
for chunk in model.generate_content("Stream 3 ways to keep study focus.", stream=True):
    if chunk.text:
        print(chunk.text, end="", flush=True)
print()

# 4) Vision (describe an image from URL)
print_section("VISION")
try:
    r2 = model.generate_content(
        [
            "Describe this image in one short line:",
            {
                "file_data": {
                    "mime_type": "image/png",
                    "file_uri": "https://storage.googleapis.com/generativeai-downloads/images/woman-and-dog.png",
                }
            },
        ]
    )
    print(r2.text)
except Exception as e:
    print("Vision test skipped or failed:", e)

print_section("DONE")
