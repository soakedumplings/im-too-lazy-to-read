import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import load_config
from storage import MessageStore
from summarizer import configure_gemini, summarize

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

store = MessageStore()

HELP_TEXT = (
    "Hi! Invite me to a group and I'll quietly keep track of new messages.\n\n"
    "When anyone runs /summarize, I'll use AI to summarize who said what "
    "since the last summary, then forget those messages.\n\n"
    "Commands:\n"
    "/summarize - summarize the conversation since the last summary\n"
    "/help - show this help"
)


def _sender_name(update: Update) -> str:
    user = update.effective_user
    if user is None:
        return "Unknown"
    return user.full_name or (f"@{user.username}" if user.username else "Unknown")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP_TEXT)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP_TEXT)


async def collect_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return
    store.add(update.effective_chat.id, _sender_name(update), update.message.text)


async def summarize_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    messages = store.pop_all(chat_id)
    await update.message.chat.send_action("typing")
    try:
        summary = summarize(messages)
    except Exception:
        logger.exception("Summarization failed")
        await update.message.reply_text(
            "Sorry, I couldn't generate a summary right now. Please try again."
        )
        return
    await update.message.reply_text(summary)


def main() -> None:
    config = load_config()
    configure_gemini(config.gemini_api_key)

    app = Application.builder().token(config.telegram_bot_token).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("summarize", summarize_command))
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.ChatType.GROUPS,
            collect_message,
        )
    )

    logger.info("Bot starting (long polling)...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
