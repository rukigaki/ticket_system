from aiogram.fsm.state import StatesGroup, State


class TicketState(StatesGroup):
    waiting_description = State()
    waiting_title = State()