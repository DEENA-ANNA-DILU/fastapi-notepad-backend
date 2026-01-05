"""
LLM integration placeholder.
Model selected: google/flan-t5-small (Hugging Face)
Actual inference can be enabled when environment supports torch.
"""

def summarize_text(text: str) -> str:
    """
    Placeholder summarization.
    Returns first ~120 characters, cut at word boundary.
    """
    words = text.split()

    if len(words) <= 20:
        return text

    summary_words = words[:20]
    return " ".join(summary_words) + "..."





"""import os
import requests

HF_API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
HF_TOKEN = os.getenv("HF_TOKEN")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}


def summarize_text(text: str):
    payload = {"inputs": text}
    response = requests.post(HF_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return "LLM service unavailable. Please try again later."

    result = response.json()
    return result[0]["summary_text"]"""

