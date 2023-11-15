from telegram import Update
from telegram.ext import Updater, MessageHandler, filters, ApplicationBuilder
import logging
import openai
import dotenv
import os

dotenv.load_dotenv()

openai.api_key = ''
bot_token = os.getenv("BOT_TOKEN")

def get_chatgpt_reply(user_message):
    # Send user message to ChatGPT
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=user_message,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )

    # Extract the reply from ChatGPT's response
    chatgpt_reply = response.choices[0].text.strip()

    return chatgpt_reply


async def handle_message(update: Update, context):
    # Get the user's message
    user_message = update.message.text
    #print(user_message)
    # Forward the user's message to ChatGPT
    chatgpt_reply = get_chatgpt_reply(user_message)

    # Send the reply back to the user
    #
    await update.message.reply_text(chatgpt_reply)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initialize the Telegram bot
botapp = ApplicationBuilder().token(bot_token).build()





# Register the message handler function
message_handler = MessageHandler(filters.TEXT, handle_message)
botapp.add_handler(message_handler)

# Start the bot
#updater.start_polling()
botapp.run_polling()