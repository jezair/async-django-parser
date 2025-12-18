from django.core.management import BaseCommand

from parsing.services.parser_service import start_books_parser


class Command(BaseCommand):
    help = "Run books parser"

    def handle(self, *args, **options):
        run = start_books_parser()
        self.stdout.write(self.style.SUCCESS(F"Parser started, run_id={run.id}"))