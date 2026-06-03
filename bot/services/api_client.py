import httpx

from bot_config import API_URL


async def get_books(page: int = 1):
    async with httpx.AsyncClient() as client:
        r = await client.get(API_URL, params={"page": page})
        return r.json()