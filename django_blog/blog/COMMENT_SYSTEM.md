# Comment Functionality Documentation

This document covers the implementation of the comment system, including the model, forms, views, and integration into the blog post detail page.

## 1. Comment Model (`blog/models.py`)

The `Comment` model establishes a **many-to-one relationship** with `Post` via a `ForeignKey`, using `related_name='comments'` to easily access all comments from a post object (`post.comments.all()`).

### Fields:
* `post`: `ForeignKey` to `Post` (What post it belongs to)
* `author`: `ForeignKey` to Django's `User` (Who wrote it)
* `content`: `TextField`
* `created_at`: `DateTimeField` (When it was created)
* `updated_at`: `DateTimeField` (When it was last updated)

## 2. Views and Integration

### `PostDetailView` Modification
The `PostDetailView` was updated using `get_context_data` to pass two key variables to the template:
1.  `comment_form`: An instance of `CommentForm` for users to submit new comments.
2.  `comments`: The queryset of all comments related to the current post (`self.object.comments.all()`).

### Comment CRUD Views
Similar to posts, comments use generic CBVs with strict permissions:
* **`CommentCreateView`**: Uses `LoginRequiredMixin`. The `form_valid` method is overridden to manually set the `author` (to the logged-in user) and the `post` (derived from the URL's primary key (`pk`)).
* **`CommentUpdateView` / `CommentDeleteView`**: Both use `LoginRequiredMixin` and **`UserPassesTestMixin`** to ensure that **only the comment's author** can modify or remove the comment.

## 3. URL Structure

Comment URLs are structured relative to the Post URL for context, but update/delete use the comment's primary key (`pk`) for identity:

| Action | URL Pattern | URL Name | PK Used |
| :--- | :--- | :--- | :--- |
| **Create** | `/posts/<int:pk>/comments/new/` | `comment_create` | Post PK |
| **Update** | `/comments/<int:pk>/edit/` | `comment_update` | Comment PK |
| **Delete** | `/comments/<int:pk>/delete/` | `comment_delete` | Comment PK |

## 4. Template Integration

The `blog/post_detail.html` template now includes:
1.  A loop (`{% for comment in comments %}`) to display all associated comments.
2.  Conditional rendering (`{% if user.is_authenticated %}`) to display the `CommentForm` for creating new comments.
3.  Conditional rendering (`{% if comment.author == user %}`) to display the Edit/Delete links next to comments only if the current user is the author.
