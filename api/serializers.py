from rest_framework import serializers
from books.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fiels = [
            "id",
            "title",
            "price",
            "rating",
            "availability",
            "category",
        ]

