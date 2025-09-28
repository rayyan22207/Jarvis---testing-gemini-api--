from config import genai

# Use flash model for fast/free-tier testing
model = genai.GenerativeModel("gemini-2.5-flash")

def ask_gemini(prompt: str) -> str:
    """Basic Gemini response"""
    response = model.generate_content(prompt)
    return response.text

def stream_gemini(prompt: str):
    """Stream Gemini response"""
    for chunk in model.generate_content(prompt, stream=True):
        if chunk.text:
            yield chunk.text
