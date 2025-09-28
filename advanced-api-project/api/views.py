from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend # Correct import for the filter backend
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

# Task 1 & 2: Generic Views for Book Model with Filtering/Searching
# =================================================================

class BookListView(generics.ListAPIView):
    """
    A ListView for retrieving all books.
    Includes filtering, searching, and ordering capabilities.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    # Add backends for filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Fields to filter on (e.g., /api/books/?publication_year=1949)
    filterset_fields = ['publication_year', 'author', 'title']
    
    # Fields to search on (e.g., /api/books/?search=Orwell)
    search_fields = ['title', 'author__name']
    
    # Fields to order by (e.g., /api/books/?ordering=-title)
    ordering_fields = ['publication_year', 'title']


class BookDetailView(generics.RetrieveAPIView):
    """A DetailView for retrieving a single book by ID."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class BookCreateView(generics.CreateAPIView):
    """A CreateView for adding a new book."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookUpdateView(generics.UpdateAPIView):
    """An UpdateView for modifying an existing book."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookDeleteView(generics.DestroyAPIView):
    """A DeleteView for removing a book."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]