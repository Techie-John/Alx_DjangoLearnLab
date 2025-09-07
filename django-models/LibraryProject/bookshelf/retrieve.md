This file documents the command and output for **retrieving** the book you just created.

```markdown
### Retrieve Operation

**Command:**
```python
from bookshelf.models import Book
book = Book.objects.get(title='1984')
print(f"Title: {book.title}, Author: {book.author}, Year: {book.publication_year}")