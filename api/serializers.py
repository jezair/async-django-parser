from rest_framework import serializers
from books.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "price",
            "rating",
            "availability",
            "category",
        ]

"""class BookSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "price",
            "rating",
            "availability",
            "category",
            "detail_url",
        )"""