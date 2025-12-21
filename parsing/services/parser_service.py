from token import AWAIT

from asgiref.sync import sync_to_async
from sqlalchemy.orm.sync import update
from unicodedata import category

from parsing.models import Book

from parsing.models import ParserRun
import asyncio
from django.utils import timezone

from parsing.parser.books_parser import BooksParser

@sync_to_async
def _save_books(run:ParserRun, books: list[dict]):
    objects = [
        Book(parser_run=run,
             title=b["title"],
             price=b["price"],
             rating=b["rating"],
             availability=b["availability"],
             category=b["category"],
             detail_url=b["detail_url"],
             )
        for b in books
    ]

    Book.objects.bulk_create(objects, ignore_conflicts=True)

@sync_to_async
def _get_run(run_id:int)->ParserRun:
    return ParserRun.objects.get(id=run_id)


@sync_to_async
def _update_run(run: ParserRun, **fields):
    for k,v in fields.items():
        setattr(run, k,v)
    run.save(update_fields=fields.keys())


async def _run_books_parser_async(run_id: int):
    run = await _get_run(run_id)

    try:
        await _update_run(run,status=ParserRun.STATUS_RUNNING)

        parser = await BooksParser.create()
        try:
            books = await parser.run()
        finally:
            await parser.close()

        await _save_books(run, books)

        await _update_run(run, status = ParserRun.STATUS_SUCCESS, finished_at = timezone.now())

    except Exception as e:
        await _update_run(run, status = ParserRun.STATUS_FAILED, error = str(e), finished_at = timezone.now())
        raise

def start_books_parser() -> ParserRun:
    run = ParserRun.objects.create(parser_name = "books_parser", status=ParserRun.STATUS_PENDING)
    asyncio.run(_run_books_parser_async(run.id))
    return run