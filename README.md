# im-too-lazy-to-read

A Telegram bot that summarizes group chat conversations with AI. Invite it to
any group; when anyone runs `/summarize`, it uses Google Gemini to summarize
**who said what** since the last summary — keeping the important details and
dropping the filler — then forgets those messages. Messages are buffered in
memory only and are never written to disk.

## Features

- `/summarize` — summarizes all messages since the previous summary, attributed by speaker.
- Works in any group the bot is invited to; usable by all members.
- No storage: the message buffer for a chat is cleared the moment it's summarized.
- Per-group isolation: each group's messages are kept and summarized separately.

## Setup

1. **Install Python 3.9+** and dependencies (a virtualenv is recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Create a Telegram bot** with [@BotFather](https://t.me/BotFather):
   - Send `/newbot`, follow the prompts, copy the bot **token**.
   - **Disable privacy mode** (required so the bot can read all group messages):
     send `/setprivacy` to BotFather, pick your bot, choose **Disable**.

3. **Get a Gemini API key** from [Google AI Studio](https://aistudio.google.com/app/apikey).

4. **Configure secrets:** copy the example env file and fill in your values:
   ```bash
   cp .env.example .env
   # then edit .env and set TELEGRAM_BOT_TOKEN and GEMINI_API_KEY
   ```

5. **Run the bot:**
   ```bash
   python bot.py
   ```

## Usage

1. Add the bot to your Telegram group (any member can use it).
2. Chat normally — the bot silently buffers new messages.
3. Anyone can run `/summarize` to get an AI summary of the conversation since
   the last summary. The buffer is then cleared (messages forgotten).
4. `/help` shows usage info.

## How it works

- `bot.py` — Telegram handlers + long-polling entry point.
- `storage.py` — in-memory, per-chat message buffer (no disk persistence).
- `summarizer.py` — builds the transcript and calls Gemini (`gemini-1.5-flash`).
- `config.py` — loads `TELEGRAM_BOT_TOKEN` and `GEMINI_API_KEY` from env/`.env`.

## Tests

```bash
pytest -v
```

## Notes

- Telegram only delivers group messages sent **after** the bot joins and only
  when privacy mode is disabled.
- If the bot restarts, any unsummarized buffered messages are lost (by design).
