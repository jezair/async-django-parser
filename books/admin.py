from django.contrib import admin
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

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)

