import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv



load_dotenv()
TOKEN = os.getenv("BOT_TOKEN", default="")

dp = Dispatcher()



async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())