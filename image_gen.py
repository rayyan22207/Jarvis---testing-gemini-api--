# image_gen.py
import os
from io import BytesIO
from typing import List
from PIL import Image

from google import genai
from google.genai import types  # noqa: F401  # (handy for advanced options)

# Prefer GOOGLE_API_KEY; fallback to GEMINI_API_KEY for your existing setup
from config import API_KEY
_API_KEY =  API_KEY
if not _API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env")

# Create client for the Gemini Developer API
client = genai.Client(api_key=API_KEY)

def generate_image(
    prompt: str,
    out_path: str = "generated.png",
    model: str = "gemini-2.5-flash-image-preview",
) -> List[str]:
    """
    Generate image(s) from text and save PNG files.
    Returns a list of saved file paths.
    """
    resp = client.models.generate_content(model=model, contents=[prompt])

    saved: List[str] = []
    i = 0
    for part in resp.candidates[0].content.parts:
        # Parts can contain text or inline image bytes; save the images
        inline = getattr(part, "inline_data", None)
        if inline and getattr(inline, "data", None):
            img = Image.open(BytesIO(inline.data))
            path = out_path if i == 0 else out_path.replace(".png", f"_{i}.png")
            img.save(path)
            saved.append(path)
            i += 1
    return saved
