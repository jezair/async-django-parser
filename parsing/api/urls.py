from django.urls import path, include

from api.views import BookListAPIView
from .views import StartParserAPIView

urlpatterns = [
    path("parser/start/", StartParserAPIView.as_view()),
    path("books/", BookListAPIView.as_view()),
]
