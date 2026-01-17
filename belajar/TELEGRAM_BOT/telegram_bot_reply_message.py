import asyncio
from telegram import Bot
import config
# Replace these with your actual credentials
BOT_TOKEN = config.BOT_TOKEN
CHAT_ID = '784391418'
TARGET_MESSAGE_ID = 67  # The ID of the message you want to reply to

async def send_targeted_message():
    # Initialize the bot
    bot = Bot(token=BOT_TOKEN)

    async with bot:
        # Sending a message as a reply to a specific ID
        await bot.send_message(
            chat_id=CHAT_ID,
            text="This is a reply to a specific message ID!",
            reply_to_message_id=TARGET_MESSAGE_ID
        )
        print(f"Message sent to Chat {CHAT_ID} targeting Message {TARGET_MESSAGE_ID}")

if __name__ == '__main__':
    asyncio.run(send_targeted_message())