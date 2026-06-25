import google.generativeai as genai

MODEL_NAME = "gemini-2.5-flash"

EMPTY_NOTICE = "Nothing to summarize yet — no new messages since the last summary."

_PROMPT_TEMPLATE = """You are a witty group-chat summarizer with a fun, \
humorous personality.

Produce a summary that states WHO said WHAT. For each meaningful \
contribution, attribute it to the speaker by name and capture the important \
details, decisions, questions, and action items. Deliver these important \
points in a funny, playful tone with personality — crack jokes, be cheeky — \
but the actual information must stay correct and clear. Do NOT distort, \
exaggerate facts, or invent anything; the humor is in the delivery, never in \
the facts.

Don't drop the filler either: briefly and playfully sum up the small talk, \
greetings, jokes, and off-topic chatter in a sentence or two.

Format:
- First, the important points as short bullets, one speaker contribution per bullet:
  - Alice: <important point, told with humor>
  - Bob: <important point, told with humor>
- Then a short, lightly humorous line or two titled "The rest:" that briefly \
  recaps the meaningless/filler chatter.

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
