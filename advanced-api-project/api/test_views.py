from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Author, Book

class BookAPITests(APITestCase):
    """
    Test suite for the Book API endpoints.
    """

    def setUp(self):
        """Set up the initial data for tests."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        self.author = Author.objects.create(name='George Orwell')
        self.book = Book.objects.create(title='1984', publication_year=1949, author=self.author)

    def test_list_books(self):
        """Ensure any user can list books."""
        url = '/api/books/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book_unauthenticated(self):
        """Ensure unauthenticated users cannot create a book."""
        url = '/api/books/create/'
        response = self.client.post(url, {'title': 'New', 'publication_year': 2023, 'author': self.author.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        """Ensure authenticated users can create a book."""
        self.client.login(username='testuser', password='testpassword')
        url = '/api/books/create/'
        data = {'title': 'Animal Farm', 'publication_year': 1945, 'author': self.author.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book_authenticated(self):
        """Ensure authenticated users can update a book."""
        self.client.login(username='testuser', password='testpassword')
        url = f'/api/books/{self.book.id}/update/'
        data = {'title': 'Nineteen Eighty-Four', 'publication_year': 1949, 'author': self.author.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Nineteen Eighty-Four')

    def test_delete_book_authenticated(self):
        """Ensure authenticated users can delete a book."""
        self.client.login(username='testuser', password='testpassword')
        url = f'/api/books/{self.book.id}/delete/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_24_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)