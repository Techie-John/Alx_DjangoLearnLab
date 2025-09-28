# api/serializers.py

from rest_framework import serializers
from .models import Author, Book
import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    It includes all fields from the Book model and adds custom validation
    to ensure the publication_year is not in the future.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """
        Check that the publication year is not in the future.
        """
        if value > datetime.date.today().year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    It includes the author's name and a nested representation of their books.
    The nested BookSerializer (books) provides a read-only list of books
    associated with the author. This demonstrates how to handle one-to-many
    relationships in a nested, readable format.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']