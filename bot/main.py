import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from dotenv import load_dotenv

from keyboards import keyboard, category_keyboard, boolean_keyboard
from utils import create_ticket


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN", default="")

dp = Dispatcher()

class TicketState(StatesGroup):
    waiting_description = State()
    waiting_title = State()


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Вы запустили бот!", reply_markup=keyboard)


@dp.callback_query(F.data == "create")
async def create_ticket_handler(callback: CallbackQuery):
    if isinstance(callback.message, Message):
        await callback.message.edit_text(text="Выберите что хотите создать", reply_markup=category_keyboard)


@dp.callback_query(F.data == "create_ticket_toilet_broke")
async def toilet_broke_handler(callback: CallbackQuery, state: FSMContext):
    await state.update_data(title=callback.data)
    await state.set_state(TicketState.waiting_description)
    await callback.message.answer("Хотите добавить описание", reply_markup=boolean_keyboard)


@dp.callback_query(F.data == "pressed_yes")
async def yes_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TicketState.waiting_description)
    await callback.message.answer("Введите желаемое описание:")


@dp.message(TicketState.waiting_description)
async def get_description_handler(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    await state.clear()
    await create_ticket(message, data["title"], desc=data["description"])


@dp.callback_query(F.data == "pressed_no")
async def no_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if isinstance(callback.message, Message):
        await create_ticket(callback.message, data["title"])

@dp.callback_query(F.data == "return_back")
async def return_back_handler(callback: CallbackQuery):
    if isinstance(callback.message, Message):
        await callback.message.edit_text(text="Вы запустили бот!", reply_markup=keyboard)


@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer("Чем вам помочь?")


async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())