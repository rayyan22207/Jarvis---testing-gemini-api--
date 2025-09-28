import re
from typing import Generator, Iterable, Optional, Union
from config import get_model

# Default model instance
model = get_model()  # uses DEFAULT_MODEL from config.py

def _clean_text(text: Optional[str]) -> str:
    """Trim, and collapse 3+ newlines to 2."""
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text

def ask_gemini(
    prompt: str,
    stream: Optional[bool] = None,
    threshold: int = 500,
    model_name: Optional[str] = None,
) -> Union[str, Generator[str, None, None]]:
    """
    Unified Gemini call with auto streaming.

    - If stream is None: stream when len(prompt) >= threshold (default 500).
    - If stream is False: return a full string.
    - If stream is True: return a generator yielding chunks.

    Args:
        prompt: user prompt
        stream: force streaming or not (None = auto)
        threshold: char count to trigger streaming when stream is None
        model_name: override default model name if needed

    Returns:
        str (non-stream) OR generator[str] (stream)
    """
    m = get_model(model_name) if model_name else model
    use_stream = (len(prompt) >= threshold) if stream is None else stream

    if use_stream:
        def _gen() -> Iterable[str]:
            for chunk in m.generate_content(prompt, stream=True):
                if chunk.text:
                    yield _clean_text(chunk.text)
        return _gen()
    else:
        resp = m.generate_content(prompt)
        return _clean_text(getattr(resp, "text", ""))

# Optional convenience wrappers (if you ever want to call explicitly)
def ask_gemini_basic(prompt: str) -> str:
    return ask_gemini(prompt, stream=False)  # type: ignore[return-value]

def ask_gemini_stream(prompt: str) -> Generator[str, None, None]:
    return ask_gemini(prompt, stream=True)   # type: ignore[return-value]

# If you want a version that ALWAYS returns a full string but still uses
# streaming under the hood for long prompts, use this:
def ask_gemini_text(
    prompt: str,
    threshold: int = 500,
    model_name: Optional[str] = None,
) -> str:
    m = get_model(model_name) if model_name else model
    if len(prompt) < threshold:
        resp = m.generate_content(prompt)
        return _clean_text(getattr(resp, "text", ""))

    # Long prompt → stream but buffer to text
    parts = []
    for chunk in m.generate_content(prompt, stream=True):
        if chunk.text:
            parts.append(chunk.text)
    return _clean_text("".join(parts))
