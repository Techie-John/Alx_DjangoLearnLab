# api/views.py

from rest_framework import generics, permissions, filters
from .models import Book
from .serializers import BookSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class BookListCreateView(generics.ListCreateAPIView):
    """
    Enhanced view to list all books or create a new one.
    - Supports filtering by publication_year and author id.
    - Supports searching on title and author's name.
    - Supports ordering by title and publication_year.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # Add filtering, searching, and ordering backends
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Fields to filter on
    filterset_fields = ['publication_year', 'author']
    
    # Fields to search on (note: author__name spans the relationship)
    search_fields = ['title', 'author__name']
    
    # Fields to order by
    ordering_fields = ['publication_year', 'title']


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a book by its ID.
    - GET: Retrieve a single book.
    - PUT/PATCH: Update a book.
    - DELETE: Delete a book.
    Permissions:
    - Allow any user to view a book's details (read-only).
    - Only authenticated users can update or delete a book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]