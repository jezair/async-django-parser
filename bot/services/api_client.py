import httpx

from bot_config import API_URL


async def get_books():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/books/")
        response.raise_for_status()

        return response.json()