# ai_writer.py
from typing import Literal, Optional
import os
from google import genai
import streamlit as st

# --------------------------------------------------------------------
# Initialise Gemini client once, re-use across calls
# --------------------------------------------------------------------
GEMINI_API_KEY = st.secrets["API"] # or hard-code for quick tests
client = genai.Client(api_key=GEMINI_API_KEY)

# --------------------------------------------------------------------
# Internal prompt builder helpers
# --------------------------------------------------------------------
STYLE_PROMPTS = {
    "default": "a clear, reader-friendly narrative style",
    "formal": "a formal, academic prose style suitable for publication",
    "creative": "an engaging, vivid storytelling style that sparks imagination",
}

def _build_writer_prompt(text: str,
                         style: Literal["default", "formal", "creative"] = "default",
                         tone: Optional[str] = None) -> str:
    """Create the prompt for the Writer agent."""
    style_desc = STYLE_PROMPTS[style]
    tone_desc = f" with a {tone} tone" if tone else ""
    return (
        "You are **Writer-Bot**, an expert AI rewriter.\n"
        "Rewrite the following chapter in " + style_desc + tone_desc + ".\n"
        "• Preserve meaning and factual content.\n"
        "• Do **NOT** add side comments, explanations, markdown, or questions.\n"
        "Return *only* the rewritten text.\n\n"
        "=== BEGIN ORIGINAL TEXT ===\n"
        f"{text}\n"
        "=== END ORIGINAL TEXT ==="
    )

def _build_reviewer_prompt(text: str) -> str:
    """Create the prompt for the Reviewer agent."""
    return (
        "You are **Reviewer-Bot**, an editorial AI.\n"
        "Refine the text below for grammar, fluency, and cohesion while keeping the author’s voice.\n"
        "Do **NOT** change facts or meaning.\n"
        "Return the improved text only, with no extra comments.\n\n"
        f"{text}"
    )

# --------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------
def generate_ai_version(text: str,
                        style: Literal["default", "formal", "creative"] = "default",
                        tone: Optional[str] = None,
                        model: str = "gemini-2.5-flash") -> str:
    """Writer agent – creative spin."""
    prompt = _build_writer_prompt(text, style=style, tone=tone)
    response = client.models.generate_content(model=model, contents=prompt)
    return response.text.strip()

def review_text(text: str,
                model: str = "gemini-2.5-flash") -> str:
    """Reviewer agent – grammar & flow."""
    prompt = _build_reviewer_prompt(text)
    response = client.models.generate_content(model=model, contents=prompt)
    return response.text.strip()
