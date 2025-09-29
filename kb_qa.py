from typing import List, Dict
from retriever import load_kb, top_k
from gemini_client import ask_gemini_text

SYSTEM_RULES = """You are a meticulous assistant.
You must answer ONLY from the provided context below. If the answer is not in context, say: "Not in knowledge base."
Always cite the item ids you used, like [c1], [g1]. Keep it concise.
"""

def make_context(snippets: List[Dict]) -> str:
    lines = []
    for it in snippets:
        lines.append(f"- [{it['id']}] {it['title']}: {it['summary']} (tags: {', '.join(it.get('tags', []))})")
    return "\n".join(lines)

def answer_from_kb(question: str, json_path: str = "data/sample.json") -> str:
    kb = load_kb(json_path)
    hits = [it for it, _ in top_k(question, kb, k=3)]
    context = make_context(hits)
    prompt = (
        f"{SYSTEM_RULES}\n\n"
        f"Context:\n{context if context else '(no relevant items)'}\n\n"
        f"Question: {question}\n\n"
        f"Answer (cite item ids you used):"
    )
    return ask_gemini_text(prompt, threshold=800)  # uses your existing helper
