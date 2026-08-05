from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from bot.keyboards import keyboard

from .services import FieldRequirementResolver
from .states import *

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Вы запустили бот!", reply_markup=keyboard)


@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer("Чем вам помочь?")


@router.message(TicketState.waiting_title)
async def get_msg_title_handler(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    # TODO: Возможно у объекта message есть какой-нибудь атрибут, который может вывести то, что обработчик на title уже был сработан, чтобы
    #  различать когда был использован put, а когда patch
    data = await state.get_data()
    method = data["method"]
    method_name = f"{method}_util_ticket"

    execute_func = getattr(FieldRequirementResolver, method_name)
    await execute_func(message, state=state, data=data)


@router.message(TicketState.waiting_description)
async def get_description_handler(message: Message, state: FSMContext):
    await state.update_data(description=message.text)

    data = await state.get_data()
    method = data["method"]
    method_name = f"{method}_util_ticket"

    execute_func = getattr(FieldRequirementResolver, method_name)
    await execute_func(message, state=state, data=data)
