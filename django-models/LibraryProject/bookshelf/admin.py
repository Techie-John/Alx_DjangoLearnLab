from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    """
    Customizes the Django admin interface for the Book model.
    """
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('publication_year', 'author')

admin.site.register(Book, BookAdmin)