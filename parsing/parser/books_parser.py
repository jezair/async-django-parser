import asyncio
from typing import List
import aiohttp
from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup
from decimal import Decimal

from django.tasks.signals import task_started
from django.utils.translation.trans_real import catalog
from sqlalchemy.sql.functions import session_user
from sqlalchemy.util import await_only
from watchfiles import awatch

from books.models import Category, Book

BASE_URL = "https://books.toscrape.com/"

class BooksParser:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    @classmethod
    async def create(cls, max_connections: int = 100):
        connector = aiohttp.TCPConnector(limit=max_connections)
        session = aiohttp.ClientSession(connector=connector,
                                        headers={
                                                "User-Agent": "Mozilla/5.0",
                                                "Accept-Language": "ru-RU,ru;q=0.9",
                                            },
                                        )
        return cls(session)

    async def close(self):
        await self.session.close()

    async def fetch(self, url: str) -> str:
        async with self.session.get(url) as response:
            response.raise_for_status()
            return await response.text()

    async def get_total_pages(self) -> int:
        html = await self.fetch(BASE_URL)
        soup = BeautifulSoup(html, "lxml")
        node = soup.select_one(".pages .current")
        if not node:
            return 1

        text = node.text.strip()

        try:
            return int(text.split("of")[-1]) # 1-50
        except ValueError:
            return 1

    async def parse_catalog_page(self, page: int) -> List[str]:
        url = f"{BASE_URL}catalogue/page-{page}.html"
        html = await self.fetch(url)
        soup = BeautifulSoup(html, "lxml")

        links = []
        for a in soup.select("article.product_pod h3 a"):
            href = a["href"].replace("../../", "")
            links.append(BASE_URL+"catalogue/"+href)

        return links


    async def parse_book_page(self, url: str) -> dict:
        html = await self.fetch(url)
        soup = BeautifulSoup(html, "lxml")

        title = soup.select_one("h1").text
        price = Decimal(soup.select_one(".price_color").text.replace("£", ""))
        availability = "In stock" in soup.select_one(".availability").text

        rating_map = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5,
        }

        rating_class = soup.select_one(".star-rating")["class"][1]
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

    async def run(self) -> List[dict]:
        total_pages = await self.get_total_pages()

        catalog_tasks = [self.parse_catalog_page(page) for page in range(1, total_pages + 1)]
        pages_results = await asyncio.gather(*catalog_tasks)
        book_urls = [url for page in pages_results for url in page]
        book_tasks = [self.parse_book_page(url) for url in book_urls]

        results = await asyncio.gather(*book_tasks, return_exceptions=True)
        saved_books=[]
        for result in results:
            if isinstance(result, Exception):
                continue

            category, _ = await sync_to_async(Category.objects.get_or_create)(name=result["category"])
            book, _ = await sync_to_async(Book.objects.update_or_create)(
                detail_url=result["detail_url"],
                defaults={
                    "title": result["title"],
                    "price": result["price"],
                    "rating": result["rating"],
                    "availability": result["availability"],
                    "category": category,
                    "detail_url": result.get("detail_url", ""),
                }
            )

            saved_books.append(book)

        await self.close()
        print(len(saved_books))
        return saved_books