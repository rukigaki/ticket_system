import httpx
from aiogram.types import Message


async def create_ticket(message: Message, title, desc="description"):
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://127.0.0.1:8000/api/tickets/",
            json={"title": title, "description": desc},
        )
    await message.answer("Тикет был успешно создан!")


async def delete_ticket(message: Message, ticket_id):
    async with httpx.AsyncClient() as client:
        await client.delete(f"http://127.0.0.1:8000/api/tickets/{ticket_id}/")

    await message.answer(f"Тикет id:{ticket_id} был успешно удален!")


async def put_ticket(message: Message, ticket_id, title, desc):
    async with httpx.AsyncClient() as client:
        await client.put(
            f"http://127.0.0.1:8000/api/tickets/{ticket_id}/",
            json={
                "title": title,
                "description": desc,
            },
        )
    await message.answer(f"Тикет id:{ticket_id} был успешно обновлен!")


async def patch_ticket(message: Message, ticket_id):
    async with httpx.AsyncClient() as client:
        await client.patch(
            f"http://127.0.0.1:8000/api/tickets/{ticket_id}/",
            json={"title": "Title was successfully updated!"},
        )

    await message.answer(f"Тикет id:{ticket_id} был успешно обновлен частично!")
