from groq import Groq
import os
import time
from typing import Any, Dict, Optional

MODEL_NAME = "llama-3.1-8b-instant"


def _get_client() -> Groq:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError("GROQ_API_KEY is not set in the environment.")
    return Groq(api_key=api_key)


def build_prompt(company: Dict[str, Any]) -> str:
    score = company.get("score", 50)

    if score >= 80:
        tone = "direct and high-confidence"
    elif score >= 60:
        tone = "friendly and value-focused"
    else:
        tone = "light networking, low pressure"

    return f"""
Write a short cold outreach email.

Company: {company['name']}
Industry: {company['industry']}
Score: {score}/100
Tone: {tone}
Pain point: {company['pain_point']}

Rules:
- under 120 words
- personalized look
- no spammy language
""".strip()


def generate_email(
    company: Dict[str, Any],
    client: Optional[Groq] = None,
    model: str = MODEL_NAME,
) -> Dict[str, Any]:
    prompt = build_prompt(company)
    client = client or _get_client()

    started_at = time.perf_counter()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    latency_ms = round((time.perf_counter() - started_at) * 1000, 2)

    return {
        "prompt": prompt,
        "email": response.choices[0].message.content,
        "latency_ms": latency_ms,
        "model": model,
    }
