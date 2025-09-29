import json, re
from typing import List, Dict, Tuple

_WORD = re.compile(r"[A-Za-z0-9_]+")

def _words(text: str) -> set:
    return set(w.lower() for w in _WORD.findall(text or ""))

def load_kb(path: str) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def score_item(query: str, item: Dict) -> float:
    """
    Super-simple lexical score: word overlap between query and (title+summary+tags).
    """
    q = _words(query)
    corpus = _words(item.get("title","") + " " + item.get("summary","") + " " + " ".join(item.get("tags",[])))
    if not q or not corpus:
        return 0.0
    overlap = q & corpus
    # Weight: overlap size + small bonus if exact phrase appears in summary
    phrase_bonus = 0.5 if any(p in item.get("summary","").lower() for p in ["real-time", "pricing", "webrtc"]) else 0.0
    return len(overlap) + phrase_bonus

def top_k(query: str, items: List[Dict], k: int = 3) -> List[Tuple[Dict, float]]:
    scored = [(it, score_item(query, it)) for it in items]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [x for x in scored[:k] if x[1] > 0]
