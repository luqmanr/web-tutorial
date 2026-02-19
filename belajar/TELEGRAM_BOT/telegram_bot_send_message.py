import asyncio
from telegram import Bot
import config

# Replace these with your actual credentials
BOT_TOKEN = config.BOT_TOKEN
CHAT_ID = config.CHAT_ID

async def send_targeted_message():
    # Initialize the bot
    bot = Bot(token=BOT_TOKEN)

    async with bot:
        # Sending a message as a reply to a specific ID
        await bot.send_message(
            chat_id=CHAT_ID,
            text="This is a reply"
        )
        print(f"Message sent to Chat {CHAT_ID}")

if __name__ == '__main__':
    asyncio.run(send_targeted_message())
    