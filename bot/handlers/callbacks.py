from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from .handlers import TicketState
from bot.keyboards import (
    keyboard,
    category_keyboard,
    boolean_keyboard,
    get_keyboard,
)
from bot.api_funcs import create_ticket, patch_ticket
from .services import DataActionResolver

router = Router()


@router.callback_query(F.data == "create")
async def create_ticket_handler(callback: CallbackQuery, state: FSMContext):
    await state.update_data(method=callback.data)
    if isinstance(callback.message, Message):
        await callback.message.edit_text(
            text="Выберите что хотите создать", reply_markup=category_keyboard
        )


@router.callback_query(F.data == "create_ticket_toilet_broke")
async def toilet_broke_handler(callback: CallbackQuery, state: FSMContext):
    await state.update_data(title=callback.data)
    await state.set_state(TicketState.waiting_description)
    await callback.message.answer(
        "Хотите добавить описание", reply_markup=boolean_keyboard
    )


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
async def tv_broke_handler(callback: CallbackQuery, state: FSMContext):
    await state.update_data(title=callback.data)
    await state.set_state(TicketState.waiting_description)
    await callback.message.answer(
        "Хотите добавить описание", reply_markup=boolean_keyboard
    )


class PaginationState(StatesGroup):
    pagination_mode = State()


@router.callback_query(F.data == "get")
async def get_ticket_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PaginationState.pagination_mode)
    await state.update_data(page=0)
    await callback.message.edit_text(
        text="Выберите тикет:", reply_markup=await get_keyboard(0)
    )


@router.callback_query(PaginationState.pagination_mode, F.data == "Вперед")
async def forward_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    page = data["page"] + 1
    await callback.message.edit_reply_markup(reply_markup=await get_keyboard(page))
    await state.update_data(page=page)


@router.callback_query(PaginationState.pagination_mode, F.data == "Назад")
async def back_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    page = data["page"] - 1
    await callback.message.edit_reply_markup(reply_markup=await get_keyboard(page))
    await state.update_data(page=page)


@router.callback_query(F.data == "return_back")
async def return_back_handler(callback: CallbackQuery):
    if isinstance(callback.message, Message):
        await callback.message.edit_text(
            text="Вы запустили бот!", reply_markup=keyboard
        )


@router.callback_query(F.data == "delete")
async def delete_ticket_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PaginationState.pagination_mode)
    await state.update_data(page=0)
    await state.update_data(method=callback.data)
    await callback.message.edit_text(
        f"Вы действительно хотите удалить тикет?", reply_markup=await get_keyboard(0)
    )


@router.callback_query(F.data.startswith("ticket_"))
async def ticket_handler(callback: CallbackQuery, state: FSMContext):
    ticket_id = int(callback.data.split("_")[1])
    await state.update_data(ticket_id=ticket_id)

    data = await state.get_data()
    method = data["method"]
    method_name = f"{method}_util_ticket"

    execute_func = getattr(DataActionResolver, method_name)
    await execute_func(callback.message, state=state, ticket_id=ticket_id)


@router.callback_query(F.data == "title")
async def get_title_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите title:")
    await state.set_state(TicketState.waiting_title)


@router.callback_query(F.data == "description")
async def get_desc_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите description:")
    await state.set_state(TicketState.waiting_description)


@router.callback_query(F.data == "patch")
async def patch_ticket_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PaginationState.pagination_mode)
    await state.update_data(page=0)
    await state.update_data(method=callback.data)
    await callback.message.edit_text(
        "Выберите тикет для частичного обновления:", reply_markup=await get_keyboard(0)
    )


@router.callback_query(F.data == "put")
async def put_ticket_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PaginationState.pagination_mode)
    await state.update_data(page=0)
    await state.update_data(method=callback.data)
    await callback.message.edit_text(
        "Выберите тикет для обновления:", reply_markup=await get_keyboard(0)
    )


@router.callback_query(F.data == "completed")
async def completed_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await patch_ticket(callback.message, data["ticket_id"])
