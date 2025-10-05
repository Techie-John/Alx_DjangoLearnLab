# Blog Post Management (CRUD) Features Documentation

This document outlines the implementation of the Create, Read, Update, and Delete (CRUD) operations for blog posts, using Django's Generic Class-Based Views (CBVs).

## 1. Implementation Overview (CBVs)

All core post management features are handled by dedicated CBVs imported from `django.views.generic`:

| Operation | CBV Class | Permissions Applied | URL Name |
| :--- | :--- | :--- | :--- |
| **List (R)** | `PostListView` | None (Public) | `post_list` (`/`) |
| **Detail (R)** | `PostDetailView` | None (Public) | `post_detail` (`/posts/<pk>/`) |
| **Create (C)** | `PostCreateView` | `LoginRequiredMixin` | `post_create` (`/posts/new/`) |
| **Update (U)** | `PostUpdateView` | `LoginRequiredMixin`, `UserPassesTestMixin` | `post_update` (`/posts/<pk>/edit/`) |
| **Delete (D)** | `PostDeleteView` | `LoginRequiredMixin`, `UserPassesTestMixin` | `post_delete` (`/posts/<pk>/delete/`) |

## 2. Permissions and Access Control (`blog/views.py`)

Access control is enforced using Mixins:

1.  **`LoginRequiredMixin`**: Ensures that a user must be logged in to access **Create**, **Update**, or **Delete** views. Unauthorized access redirects to the login page.
2.  **`UserPassesTestMixin`**: Applied to **Update** and **Delete** views. This mixin requires the **`test_func()`** method to return `True` for the request to proceed.
    * **`test_func()` Logic**: `return self.request.user == post.author` ensures that only the original author of the post can edit or delete it.

## 3. Post-Action Redirection

* **Create/Update**: The `Post` model includes a `get_absolute_url()` method. Upon successful creation or update, the view uses this method to redirect the user directly to the new post's detail page.
* **Delete**: The `PostDeleteView` uses `success_url = reverse_lazy('post_list')` to redirect the user back to the main blog list after a post is successfully deleted.