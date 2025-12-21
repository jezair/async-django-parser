from django.contrib import admin
from sqlalchemy.engine import ConnectArgsType

from .models import Book, Category

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "price",
        "rating",
        "availability",
    )

    list_filter = ("category", "rating", "availability")
    search_fields = ("title",)
    ordering = ("price",)

    list_per_page = 1000

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)
