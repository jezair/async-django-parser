from rest_framework import generics
from books.models import Book
from .serializers import BookSerializer
from .filters import BookFilter

class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilter