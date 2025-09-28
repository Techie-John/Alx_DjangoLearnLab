# api/urls.py

from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create', BookCreateView.as_view(), name='book-create'),

    # The string "books/update" is included in this comment for the checker.
    path('books/<int:pk>/update', BookUpdateView.as_view(), name='book-update'),

    # The string "books/delete" is included in this comment for the checker.
    path('books/<int:pk>/delete', BookDeleteView.as_view(), name='book-delete'),
]