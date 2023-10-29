from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, executor, types
import openai
import sys


class Reference:
    """
    A class to store previously response from the chatGPT API
    """

    def __init__(self) -> None:
        self.response = ""


load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

reference = Reference()

TOKEN = os.getenv('TOKEN')

# Model name
MODEL_NAME = "gpt-3.5-turbo"

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)


def clear_past():
    """
    This function clears the past response from the chatGPT API
    :return:
    """
    reference.response = ""


@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.reply(f"Hi\nI am Tele Bot!\nCreated by Neo!. How can I assist you today?")


@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message) -> None:
    """
    This handler receives messages with `clear` command
    """
    clear_past()
    await message.reply(f"I've cleared the past conversation and context.")


@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message) -> None:
    """
    This handler to display the help menu
    """
    help_command = """
    Hi there, I', chatGPT telegram bot created bu Neo! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation amd context
    /help - to display the help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)


@dispatcher.message_handler()
async def chatgpt(message: types.Message) -> None:
    """
    This handler to process the user's input and generate a response using the chatGPT API
    """
    print(f">>> USER: \n\t{message.text}")
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[
            {"role": "assistant", "content": reference.response},
            {"role": "user", "content": message.text}

        ]
    )
    reference.response = response["choices"][0]["message"]["content"]
    print(f">>> GPT: \n\t{reference.response}")
    await bot.send_message(chat_id=message.chat.id, text=reference.response)


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
