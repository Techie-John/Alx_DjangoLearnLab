# api/tests.py

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Author, Book

class BookAPITests(APITestCase):
    """
    Test suite for the Book API endpoints.
    Covers CRUD, filtering, searching, and ordering functionalities.
    """

    def setUp(self):
        """
        Set up the initial data for tests.
        This runs before each test method.
        """
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Create authors and books
        self.author1 = Author.objects.create(name='George Orwell')
        self.author2 = Author.objects.create(name='Aldous Huxley')
        
        self.book1 = Book.objects.create(title='1984', publication_year=1949, author=self.author1)
        self.book2 = Book.objects.create(title='Animal Farm', publication_year=1945, author=self.author1)
        self.book3 = Book.objects.create(title='Brave New World', publication_year=1932, author=self.author2)
        
        # URLs
        self.list_create_url = '/api/books/'
        self.detail_url = f'/api/books/{self.book1.id}/'

    def test_list_books_unauthenticated(self):
        """Ensure unauthenticated users can list books."""
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_book_unauthenticated(self):
        """Ensure unauthenticated users cannot create a book."""
        data = {'title': 'New Book', 'publication_year': 2025, 'author': self.author1.id}
        response = self.client.post(self.list_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        """Ensure authenticated users can create a book."""
        self.client.login(username='testuser', password='testpassword')
        data = {'title': 'New Book', 'publication_year': 2025, 'author': self.author1.id}
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(Book.objects.latest('id').title, 'New Book')

    def test_update_book_authenticated(self):
        """Ensure authenticated users can update a book."""
        self.client.login(username='testuser', password='testpassword')
        data = {'title': 'Nineteen Eighty-Four', 'publication_year': 1949, 'author': self.author1.id}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Nineteen Eighty-Four')

    def test_delete_book_authenticated(self):
        """Ensure authenticated users can delete a book."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)

    def test_filter_by_publication_year(self):
        """Test filtering books by publication year."""
        response = self.client.get(f'{self.list_create_url}?publication_year=1945')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Animal Farm')

    def test_search_by_author_name(self):
        """Test searching books by author's name."""
        response = self.client.get(f'{self.list_create_url}?search=Huxley')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Brave New World')

    def test_order_by_title(self):
        """Test ordering books by title."""
        response = self.client.get(f'{self.list_create_url}?ordering=title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], '1984')
        self.assertEqual(response.data[1]['title'], 'Animal Farm')