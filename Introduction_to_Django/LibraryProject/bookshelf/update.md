This file documents the command and output for **updating** the book's title.

```markdown
### Update Operation

**Command:**
```python
from bookshelf.models import Book
book = Book.objects.get(title='1984')
book.title = 'Nineteen Eighty-Four'
book.save()
book