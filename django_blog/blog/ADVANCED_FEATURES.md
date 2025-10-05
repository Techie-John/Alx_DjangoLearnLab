# Advanced Features: Tagging and Search Functionality

This document details the implementation of tagging using `django-taggit` and the custom search functionality using Django's `Q` objects.

## 1. Tagging Implementation (`django-taggit`)

### Setup:
1.  The `taggit` package was installed and added to `INSTALLED_APPS` in `settings.py`.
2.  The `Post` model in `blog/models.py` was extended with: `tags = TaggableManager()`. This automatically creates the necessary intermediary database tables.

### Usage:
* **Forms**: `PostCreateView` and `PostUpdateView` automatically expose the `tags` field, allowing users to input tags as a comma-separated list during post creation/editing.
* **Template Display**: Tags are retrieved using `post.tags.all()` in the `post_detail.html` template.
* **Tag Filtering View**: The custom `post_by_tag_view` filters the `Post` queryset using `tags__slug__in=[tag_slug]`, allowing users to click a tag to see all related posts.

### URL Structure (Tagging):
* **URL**: `/tags/<str:tag_slug>/`
* **URL Name**: `posts_by_tag`

## 2. Search Functionality

### Search View (`search_results_view` in `blog/views.py`)

The search is handled by a single function-based view that accepts a query parameter `q` from the URL.

The search logic is implemented using **`django.db.models.Q` objects** to combine multiple lookups with an **OR** logical operator (`|`).

### Query Logic:

The search query filters posts where the query matches:
1.  **Title**: `Q(title__icontains=query)` (case-insensitive)
2.  **Content**: `Q(content__icontains=query)` (case-insensitive)
3.  **Tags**: `Q(tags__name__in=[query])` (Checks if the query matches an exact tag name)

The `distinct()` method is applied to prevent duplicate posts from appearing if they match multiple criteria (e.g., matching the title and one of the tags).

### URL Structure (Search):
* **URL**: `/search/`
* **URL Name**: `search_results` (Accessed via the search bar in `base.html` using `GET` request)