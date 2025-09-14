from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

class ExampleForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)
    email = forms.EmailField(label="Your email")        