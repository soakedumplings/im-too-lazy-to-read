import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    telegram_bot_token: str
    gemini_api_key: str


def load_config() -> Config:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    key = os.getenv("GEMINI_API_KEY")
    missing = [name for name, val in
               (("TELEGRAM_BOT_TOKEN", token), ("GEMINI_API_KEY", key))
               if not val]
    if missing:
        raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")
    return Config(telegram_bot_token=token, gemini_api_key=key)
