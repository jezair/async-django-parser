from django.contrib import admin
from parsing.models import Book, ParserRun

@admin.register(Book)
class BooksAdmin(admin.ModelAdmin):
    list_display = ("title","price","rating","availability","category","parser_run")
    list_filter = ("category","rating","availability")
    search_fields = ("title", "category")
    ordering = ("-created_at",)
    list_per_page = 1000

@admin.register(ParserRun)
class ParserRunAdmin(admin.ModelAdmin):
    list_display = ("id","parser_name","status","started_at","finished_at")
    list_filter = ("status",)

