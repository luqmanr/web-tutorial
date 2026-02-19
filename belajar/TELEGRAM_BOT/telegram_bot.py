import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

import config

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    chat_id = update.message.chat_id

    if str(chat_id) == config.CHAT_ID:
        await update.message.reply_html(
            f"Halo, cuma kamu yang bisa kasih perintah ke saya, {user.mention_html()}! Selamat datang di bot saya. Kamu bisa mengirimkan pesan apa saja, dan saya akan membalasnya dengan jumlah karakter yang kamu kirimkan.",
        )
    else:
        await update.message.reply_html(
            f"Hi {user.mention_html()} with chat_id: {chat_id} I'm an echo bot. Send me any text message!",
        )

async def update_table(update: Update, context: CallbackContext) -> None:
    await update.message.reply_html(
        f"Table has been updated successfully! Tapi BOHONG :D {update.message.text}",
    )

async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text + f" jumlah character {len(update.message.text)}")

def main() -> None:
    BOT_TOKEN = config.BOT_TOKEN

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("update_table", update_table))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("Bot started. Press Ctrl-C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
