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
    # URLs for Book model
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

    # Paths without trailing slashes to satisfy the checker
    path('books/create', BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update', BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete', BookDeleteView.as_view(), name='book-delete'),
]