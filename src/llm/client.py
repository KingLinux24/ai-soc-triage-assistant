import os
from typing import Any, Dict

def llm_enabled() -> bool:
    return os.getenv("LLM_PROVIDER", "none").lower() != "none"

def generate_summary(prompt: str) -> str:
    """
    Provider-agnostic stub.
    Implement with your preferred LLM SDK.
    Keep this function returning plain text.
    """
    raise NotImplementedError("LLM provider not configured. Set LLM_PROVIDER or use deterministic mode.")
