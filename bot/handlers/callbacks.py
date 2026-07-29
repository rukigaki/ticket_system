from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from .handlers import TicketState
from bot.keyboards import keyboard, category_keyboard, boolean_keyboard
from bot.utils import create_ticket



router = Router()

@router.callback_query(F.data == "create")
async def create_ticket_handler(callback: CallbackQuery):
    if isinstance(callback.message, Message):
        await callback.message.edit_text(text="Выберите что хотите создать", reply_markup=category_keyboard)


@router.callback_query(F.data == "create_ticket_toilet_broke")
async def toilet_broke_handler(callback: CallbackQuery, state: FSMContext):
    await state.update_data(title=callback.data)
    await state.set_state(TicketState.waiting_description)
    await callback.message.answer("Хотите добавить описание", reply_markup=boolean_keyboard)


@router.callback_query(F.data == "pressed_yes")
async def yes_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TicketState.waiting_description)
    await callback.message.answer("Введите желаемое описание:")


@router.callback_query(F.data == "pressed_no")
async def no_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if isinstance(callback.message, Message):
        await create_ticket(callback.message, data["title"])

@router.callback_query(F.data == "create_ticket_tv_broke")
async def tv_broke_handler(callback: CallbackQuery):
    await create_ticket(callback.data)


@router.callback_query(F.data == "return_back")
async def return_back_handler(callback: CallbackQuery):
    if isinstance(callback.message, Message):
        await callback.message.edit_text(text="Вы запустили бот!", reply_markup=keyboard)


@router.callback_query(F.data == "delete")
async def delete_ticket(callback: CallbackQuery):
    await callback.message.answer("Тикет удален")