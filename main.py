import logging

from config import TOKEN, eligible_users
from telegram import Update
from telegram.ext import Application, MessageHandler, \
    ContextTypes, CommandHandler, filters
from gpt_api import request_to_gpt

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

# Set higher logging level for httpx to avoid all
# GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


welcome_text = "What do you want to know?"
not_eligible_user_text = "Sorry, you are not eligible to use this bot"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context._user_id in eligible_users.values():
        await context.bot.send_message(
            context._chat_id,
            welcome_text
            )
    else:
        await context.bot.send_message(
            context._chat_id,
            not_eligible_user_text
            )


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context._user_id in eligible_users.values():
        text = update.message.text
        response = request_to_gpt(text)
        await update.message.reply_text(response)
    else:
        await context.bot.send_message(
            context._chat_id,
            not_eligible_user_text
            )


async def handle_invalid_type(
        update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if context._user_id in eligible_users.values():
        await update.message.reply_text("Где-то ошибка. Попробуйте ещё раз.")
        await context.bot.send_message(context._chat_id, welcome_text)
    else:
        await context.bot.send_message(
            context._chat_id,
            not_eligible_user_text
            )


def main() -> None:
    """Run the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~(filters.COMMAND),
                                           answer
                                           )
                            )
    application.add_handler(MessageHandler(filters.ALL, handle_invalid_type))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
