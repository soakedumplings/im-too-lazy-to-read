import logging

import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

logger = logging.getLogger(__name__)

# Tried in order. Each Gemini model has its own quota, so if one is
# rate-limited / exhausted (HTTP 429) we fall back to the next.
MODEL_NAMES = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
]

EMPTY_NOTICE = "Nothing to summarize yet — no new messages since the last summary."

_PROMPT_TEMPLATE = """You are a group-chat summarizer. Be extremely concise.

List ONLY the few genuinely important points (key decisions, questions, action \
items). Aim for at most 5 bullets — fewer is better. Each bullet is one short \
phrase (not a sentence), attributed to the speaker. Skip everything trivial. \
Never distort, exaggerate, or invent.

Format:
- One bullet per main point, blank line between bullets:

  - Alice: <short phrase>

  - Bob: <short phrase>

- End with ONE short witty line titled "The rest:" summarizing the unimportant \
  chatter in a few words. Omit this line if there's nothing worth noting.

Conversation transcript:
{transcript}
"""


def configure_gemini(api_key: str) -> None:
    genai.configure(api_key=api_key)


def build_transcript(messages: list[tuple[str, str]]) -> str:
    return "\n".join(f"{sender}: {text}" for sender, text in messages)


def summarize(messages: list[tuple[str, str]]) -> str:
    if not messages:
        return EMPTY_NOTICE
    transcript = build_transcript(messages)
    prompt = _PROMPT_TEMPLATE.format(transcript=transcript)
    last_error: Exception | None = None
    for model_name in MODEL_NAMES:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except ResourceExhausted as exc:
            logger.warning("Model %s quota exhausted, trying next", model_name)
            last_error = exc
    raise RuntimeError("All Gemini models are rate-limited") from last_error
