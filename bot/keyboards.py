from math import ceil

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async

from tickets.models import Ticket

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Create", callback_data="create"),
            InlineKeyboardButton(text="Delete", callback_data="delete"),
        ],
        [
            InlineKeyboardButton(text="Get", callback_data="get"),
            InlineKeyboardButton(text="List", callback_data="list"),
        ],
        [
            InlineKeyboardButton(text="Patch", callback_data="patch"),
            InlineKeyboardButton(text="Put", callback_data="put"),
        ],
    ]
)

category_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Бочок потик", callback_data="create_ticket_toilet_broke"
            ),
            InlineKeyboardButton(
                text="Телевизор поломался", callback_data="create_ticket_tv_broke"
            ),
            InlineKeyboardButton(text="Вернуться назад", callback_data="return_back"),
        ]
    ]
)


boolean_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Yes", callback_data="pressed_yes"),
            InlineKeyboardButton(text="No", callback_data="pressed_no"),
        ]
    ]
)


attr_model_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Title", callback_data="title"),
            InlineKeyboardButton(text="Description", callback_data="description"),
        ]
    ]
)

attr_model_keyboard_new = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Title", callback_data="title"),
            InlineKeyboardButton(text="Description", callback_data="description"),
            InlineKeyboardButton(text="Завершить", callback_data="completed")
        ]
    ]
)


@sync_to_async
def get_tickets(start, end):
    return list(Ticket.objects.filter(id__range=(start, end)))


@sync_to_async
def get_tickets_all():
    return list(Ticket.objects.all())


BACK = InlineKeyboardButton(text="<-", callback_data="Назад")
NEXT = InlineKeyboardButton(text="->", callback_data="Вперед")


async def get_keyboard(page):
    all_ticket = len(await get_tickets_all())
    all_page = ceil(all_ticket / 3)
    page %= all_page

    start = (page * 3) + 1
    end = start + 2

    tickets = await get_tickets(start, end)
    ticket_buttons = [
        InlineKeyboardButton(text=str(button), callback_data=f"ticket_{button.id}")
        for button in tickets
    ]
    my_keyboard = InlineKeyboardMarkup(inline_keyboard=[[BACK, *ticket_buttons, NEXT]])
    return my_keyboard
