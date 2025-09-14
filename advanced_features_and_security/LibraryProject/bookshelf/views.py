from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView
from .models import Book
from .forms import BookForm
from .forms import ExampleForm

# Class-based view for listing books
class BookListView(PermissionRequiredMixin, ListView):
    model = Book
    template_name = 'bookshelf/book_list.html'
    context_object_name = 'books'
    permission_required = 'bookshelf.can_view'

# Function-based view for creating a book
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            # The ORM handles data sanitization, preventing SQL injection
            book = form.save(commit=False)
            # Assign the currently logged-in user as the one who added the book
            book.added_by = request.user
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})

# Function-based view for editing a book
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form})

# Function-based view for deleting a book
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

def form_example(request):
    form = ExampleForm()
    return render(request, "bookshelf/form_example.html", {"form": form})

