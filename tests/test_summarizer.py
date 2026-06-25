from unittest.mock import MagicMock, patch

import summarizer
from summarizer import build_transcript, summarize, EMPTY_NOTICE


def test_build_transcript_formats_lines():
    msgs = [("Alice", "let's ship friday"), ("Bob", "ok sounds good")]
    assert build_transcript(msgs) == "Alice: let's ship friday\nBob: ok sounds good"


def test_summarize_empty_returns_notice():
    assert summarize([]) == EMPTY_NOTICE


def test_summarize_calls_gemini_and_returns_text():
    fake_response = MagicMock()
    fake_response.text = "Alice proposed shipping Friday; Bob agreed."
    fake_model = MagicMock()
    fake_model.generate_content.return_value = fake_response

    with patch.object(summarizer.genai, "GenerativeModel", return_value=fake_model):
        result = summarize([("Alice", "let's ship friday"), ("Bob", "ok")])

    assert result == "Alice proposed shipping Friday; Bob agreed."
    # Prompt must include the transcript so the model sees who said what
    sent_prompt = fake_model.generate_content.call_args[0][0]
    assert "Alice: let's ship friday" in sent_prompt
