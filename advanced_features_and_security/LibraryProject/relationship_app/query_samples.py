import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Create sample data for a clean run
Author.objects.all().delete()
Book.objects.all().delete()
Library.objects.all().delete()
Librarian.objects.all().delete()

author1 = Author.objects.create(name="J.K. Rowling")
author2 = Author.objects.create(name="Stephen King")

book1 = Book.objects.create(title="Harry Potter and the Sorcerer's Stone", author=author1)
book2 = Book.objects.create(title="The Shining", author=author2)
book3 = Book.objects.create(title="It", author=author2)

library1 = Library.objects.create(name="Central Library")
library1.books.add(book1, book2)

library2 = Library.objects.create(name="City Library")
library2.books.add(book2, book3)

librarian1 = Librarian.objects.create(name="Alice", library=library1)
librarian2 = Librarian.objects.create(name="Bob", library=library2)


# Query all books by a specific author
author_name = "Stephen King"
try:
    author = Author.objects.get(name=author_name)
    books_by_author = Book.objects.filter(author=author)
    print(f"Books by {author_name}:")
    for book in books_by_author:
        print(f"- {book.title}")
except Author.DoesNotExist:
    print(f"Author '{author_name}' not found.")

# List all books in a library
library_name = "Central Library"
library = Library.objects.get(name=library_name)
books_in_library = library.books.all()
print(f"\nBooks in {library_name}:")
for book in books_in_library:
    print(f"- {book.title}")

# Retrieve the librarian for a library
library_name = "Central Library"
try:
    librarian = Librarian.objects.get(library=library1)
    print(f"\nLibrarian for '{library_name}': {librarian.name}")
except Librarian.DoesNotExist:
    print(f"\nNo librarian found for '{library_name}'.")