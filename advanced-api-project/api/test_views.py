# api/test_views.py

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Author, Book

class BookAPITests(APITestCase):
    """
    Test suite for the Book API endpoints, including checks on response data.
    """

    def setUp(self):
        """Set up the initial data for tests."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.author = Author.objects.create(name='George Orwell')
        self.book = Book.objects.create(title='1984', publication_year=1949, author=self.author)

    def test_list_books(self):
        """Ensure any user can list books and the data is correct."""
        url = '/api/books/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # CHECK ADDED: Verify the content of the response data
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')

    def test_create_book_authenticated(self):
        """Ensure authenticated users can create a book and check response data."""
        self.client.login(username='testuser', password='testpassword')
        url = '/api/books/create'
        data = {'title': 'Animal Farm', 'publication_year': 1945, 'author': self.author.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # CHECK ADDED: Verify the created object's data is in the response
        self.assertEqual(response.data['title'], 'Animal Farm')
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book_authenticated(self):
        """Ensure authenticated users can update a book and check response data."""
        self.client.login(username='testuser', password='testpassword')
        url = f'/api/books/{self.book.id}/update'
        data = {'title': 'Nineteen Eighty-Four', 'publication_year': 1949, 'author': self.author.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # CHECK ADDED: Verify the updated data is in the response
        self.assertEqual(response.data['title'], 'Nineteen Eighty-Four')
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Nineteen Eighty-Four')

    def test_delete_book_authenticated(self):
        """Ensure authenticated users can delete a book."""
        self.client.login(username='testuser', password='testpassword')
        url = f'/api/books/{self.book.id}/delete'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_create_book_unauthenticated(self):
        """Ensure unauthenticated users cannot create a book."""
        url = '/api/books/create'
        response = self.client.post(url, {'title': 'New', 'publication_year': 2023, 'author': self.author.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)