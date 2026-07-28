import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv

from keyboards import keyboard


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN", default="")

dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Вы запустили бот!", reply_markup=keyboard)

@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer("Чем вам помочь?")


async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())