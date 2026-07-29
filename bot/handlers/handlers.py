from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from bot.keyboards import keyboard
from bot.utils import create_ticket


class TicketState(StatesGroup):
    waiting_description = State()
    waiting_title = State()

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Вы запустили бот!", reply_markup=keyboard)


@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer("Чем вам помочь?")


@router.message(TicketState.waiting_description)
async def get_description_handler(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    await state.clear()
    await create_ticket(message, data["title"], desc=data["description"])