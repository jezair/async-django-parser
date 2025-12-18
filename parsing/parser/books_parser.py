import asyncio
from typing import List
import aiohttp
from bs4 import BeautifulSoup
from decimal import Decimal

from django.tasks.signals import task_started
from django.utils.translation.trans_real import catalog
from watchfiles import awatch

BASE_URL = "https://books.toscrape.com/"

class BooksParser:
    def __init__(self, max_connections: int = 100):
        connector = aiohttp.TCPConnector(limit=max_connections)
        self.session = aiohttp.ClientSession(connector=connector)

    @classmethod
    async def create(cls):
        return cls()

    async def fetch(self, url = str) -> str:
        async with self.session.get(url) as response:
            response.raise_for_status()
            return await response.text()

    async def get_total_pages(self) -> int:
        html = await self.fetch(BASE_URL)
        soup = BeautifulSoup(html, "lxml")
        text = soup.select_one(".pages .current").text.strip()

        return int(text.split("of")[-1]) # 1-50

    async def parse_catalog_page(self, page: int) -> List[str]:
        url = f"{BASE_URL}catalogue/page-{page}.html"
        html = await self.fetch(url)
        soup = BeautifulSoup(html, "lxml")

        links = []
        for a in soup.select("article.product_pod h3 a"):
            href = a["href"].replace("../", "")
            links.append(BASE_URL+href)

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
        books = await asyncio.gather(*book_tasks)

        await self.close()
        return books