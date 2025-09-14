This file documents the command and output for **deleting** the book instance.

```markdown
### Delete Operation

**Command:**
```python
from bookshelf.models import Book
book = Book.objects.get(title='Nineteen Eighty-Four')
book.delete()
Book.objects.all()