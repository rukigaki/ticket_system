from bot.api_funcs import *
from .states import TicketState
from bot.keyboards import attr_model_keyboard, attr_model_keyboard_new


class DataActionResolver:
    @staticmethod
    async def create_util_ticket(message, ticket_id):
        pass

    @staticmethod
    async def put_util_ticket(message: Message, **kwargs):
        await kwargs["state"].set_state(TicketState.waiting_title)
        await message.answer("Введите title:")

    @staticmethod
    async def patch_util_ticket(message, **kwargs):
        await message.answer("Что желаете обновить?", reply_markup=attr_model_keyboard)

    @staticmethod
    async def delete_util_ticket(message, **kwargs):
        await delete_ticket(message, kwargs["ticket_id"])


class FieldRequirementResolver:
    @staticmethod
    async def create_util_ticket(message: Message, data, **kwargs):
        await create_ticket(message, data["title"], desc=data["description"])

    @staticmethod
    async def put_util_ticket(message: Message, **kwargs):
        data = kwargs["data"]
        if not data.get("description", 0):
            await kwargs["state"].set_state(TicketState.waiting_description)
            await message.answer("Введите Description:")
        else:
            await put_ticket(
                message, data["ticket_id"], data["title"], data["description"]
            )
            await kwargs["state"].clear()

    @staticmethod
    async def patch_util_ticket(message, **kwargs):
        await message.answer(
            "Что желаете обновить?", reply_markup=attr_model_keyboard_new
        )
