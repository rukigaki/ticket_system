import httpx
from aiogram.types import Message


async def create_ticket(message: Message, title, desc="description"):
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://127.0.0.1:8000/api/tickets/",
            json={"title": title, "description": desc},
        )
    await message.answer("Тикет был успешно создан!")
