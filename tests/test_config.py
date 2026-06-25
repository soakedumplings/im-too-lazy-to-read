import pytest
from config import load_config


def test_load_config_reads_env(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "tok123")
    monkeypatch.setenv("GEMINI_API_KEY", "gem456")
    cfg = load_config()
    assert cfg.telegram_bot_token == "tok123"
    assert cfg.gemini_api_key == "gem456"


def test_load_config_missing_raises(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(RuntimeError) as exc:
        load_config()
    assert "TELEGRAM_BOT_TOKEN" in str(exc.value)
    assert "GEMINI_API_KEY" in str(exc.value)
