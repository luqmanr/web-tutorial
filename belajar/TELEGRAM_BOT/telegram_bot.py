import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# --- Command Handlers ---

async def start(update: Update, context: CallbackContext) -> None:
    """Sends a welcome message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! I'm an echo bot. Send me any text message!",
    )

async def echo(update: Update, context: CallbackContext) -> None:
    """Echoes the user message."""
    # update.message.text contains the text sent by the user
    await update.message.reply_text(update.message.text)

# --- Main Function ---

def main() -> None:
    """Start the bot."""
    # Replace "YOUR_BOT_TOKEN" with your actual bot token from BotFather
    # For security, you might want to load this from an environment variable
    # or a configuration file in a real application.
    BOT_TOKEN = "YOUR_BOT_TOKEN" 

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    # CommandHandler handles commands (e.g., /start)
    application.add_handler(CommandHandler("start", start))

    # MessageHandler handles regular messages.
    # filters.TEXT ensures it only processes text messages.
    # ~filters.COMMAND ensures it doesn't process commands as regular text.
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    logger.info("Bot started. Press Ctrl-C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
