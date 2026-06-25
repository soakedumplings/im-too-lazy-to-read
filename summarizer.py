import google.generativeai as genai

MODEL_NAME = "gemini-2.5-flash"

EMPTY_NOTICE = "Nothing to summarize yet — no new messages since the last summary."

_PROMPT_TEMPLATE = """You are summarizing a group chat conversation.

Produce a concise summary that states WHO said WHAT. For each meaningful \
contribution, attribute it to the speaker by name. Capture the important \
details, decisions, questions, and action items that an intelligent reader \
would care about. Aggressively drop filler, greetings, small talk, and \
off-topic chatter — either omit it or compress it into a single short line.

Format as short bullet points, one speaker contribution per bullet, like:
- Alice: <important point>
- Bob: <important point>

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
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    return response.text
