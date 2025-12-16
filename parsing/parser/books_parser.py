import asyncio
from typing import List
import aiohttp
from bs4 import BeautifulSoup
from decimal import Decimal

from django.tasks.signals import task_started
from watchfiles import awatch

BASE_URL = "https://books.toscrape.com/"

class BooksParser:
    default_concurrency = 20

    def __init__(self, concurrency: int = default_concurrency):
        self.semaphore = asyncio.Semaphore(concurrency)

    @classmethod
    async def create(cls, concurrency: int = default_concurrency):
        return cls(concurrency=concurrency)

    async def fetch(self, session: aiohttp.ClientSession, url = str) -> str:
        async with self.semaphore:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.text()

    async def parse_catalog_page(self, session, url: str) -> List[str]:
        html = await self.fetch(session, url)
        soup = BeautifulSoup(html, "lxml")

        title = soup.select_one("h1").text
        price = soup.select_one(".price_color").text.replace("£", "")
        availability = "In stock" in soup.select_one(".availability").text

        rating_class = soup.select_one(".star-rating")["class"]
        rating_map = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5,
        }

        rating = rating_map.get(rating_class[1], 0)

        category = soup.select("ul.breadcrumb li a")[2].text

        return {
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
            "category": category,
            "detail_url": url,
        }

    async def run(self, pages: int = 2) -> List[dict]:
        async with aiohttp.ClientSession() as session:
            catalog_urls = [f"{BASE_URL}catalogue/page-{i}.html" for i in range(1,pages + 1)]

            book_urls = []
            for url in catalog_urls:
                book_urls.extend(await self.parse_catalog_page(session,url))

            tasks = [self.parse_catalog_page(session, url) for url in book_urls]

            return await asyncio.gather(*tasks)