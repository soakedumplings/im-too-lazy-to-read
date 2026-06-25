import google.generativeai as genai

MODEL_NAME = "gemini-2.5-flash"

EMPTY_NOTICE = "Nothing to summarize yet — no new messages since the last summary."

_PROMPT_TEMPLATE = """You are a group-chat summarizer. Your main job is to \
convey the important information clearly and concisely.

State WHO said WHAT: for each meaningful contribution, attribute it to the \
speaker by name and capture the important details, decisions, questions, and \
action items. Keep it concise and accurate — do NOT distort, exaggerate, or \
invent anything.

Tone: mostly neutral and to-the-point. Only add a light, witty touch when \
there's genuinely something funny or amusing in the conversation worth a \
quip — otherwise just summarize plainly. Don't force jokes.

Format:
- The important points as short bullets, one speaker contribution per bullet, \
  with a blank line between each bullet for readability:

  - Alice: <concise important point>

  - Bob: <concise important point>

- If there was notable small talk or off-topic chatter, add one short line \
  titled "The rest:" briefly recapping it. Skip this line if there's nothing \
  worth mentioning.

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
