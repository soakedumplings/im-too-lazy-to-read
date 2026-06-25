from unittest.mock import MagicMock, patch

import pytest
from google.api_core.exceptions import ResourceExhausted

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


def test_summarize_falls_back_when_first_model_exhausted():
    exhausted_model = MagicMock()
    exhausted_model.generate_content.side_effect = ResourceExhausted("429 quota")
    ok_response = MagicMock()
    ok_response.text = "fallback summary"
    ok_model = MagicMock()
    ok_model.generate_content.return_value = ok_response

    with patch.object(
        summarizer.genai, "GenerativeModel", side_effect=[exhausted_model, ok_model]
    ):
        result = summarize([("Alice", "hi")])

    assert result == "fallback summary"


def test_summarize_raises_when_all_models_exhausted():
    exhausted_model = MagicMock()
    exhausted_model.generate_content.side_effect = ResourceExhausted("429 quota")

    with patch.object(
        summarizer.genai, "GenerativeModel", return_value=exhausted_model
    ):
        with pytest.raises(RuntimeError):
            summarize([("Alice", "hi")])
