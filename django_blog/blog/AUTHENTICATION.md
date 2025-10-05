# User Authentication System Documentation

This document details the implementation of user registration, login, logout, and profile management for the Django Blog application, based on Task 1 of the project.

---

## 1. Implementation Strategy

The authentication system leverages **Django's built-in authentication views** (`auth_views`) for secure login/logout and implements **custom views and forms** for registration and profile editing.

| Feature | Type | View/Form | URL Path |
| :--- | :--- | :--- | :--- |
| **Registration** | Custom | `register_view` / `CustomUserCreationForm` | `/register/` |
| **Login** | Built-in | `auth_views.LoginView` | `/login/` |
| **Logout** | Built-in | `auth_views.LogoutView` | `/logout/` |
| **Profile Management** | Custom | `profile_view` / `UserUpdateForm` | `/profile/` |

---

## 2. Key Code Components

### `blog/forms.py`

* **`CustomUserCreationForm`**: Extends Django's base `UserCreationForm` to explicitly include the **`email`** field during registration, which is required.
* **`UserUpdateForm`**: Extends `UserChangeForm` to allow authenticated users to modify their `email`, `first_name`, and `last_name`. The sensitive password field is explicitly removed from this form for security, enforcing password changes to be handled separately.

### `blog/views.py`

* **`register_view(request)`**:
    * Handles `POST` requests using `CustomUserCreationForm`.
    * Logs the user in automatically upon successful registration (`django.contrib.auth.login`).
    * Uses Django's `messages` framework to provide feedback.
* **`profile_view(request)`**:
    * Decorated with **`@login_required`** to restrict access to authenticated users only.
    * Handles `POST` requests to update the logged-in user's details using `UserUpdateForm`.
    * Uses Django's `messages` for success/error alerts.

### `blog/urls.py`

* The file imports `views as auth_views` from `django.contrib.auth`.
* The login and logout paths use the `.as_view()` method on the built-in class-based views, specifying the `template_name` for correct rendering (e.g., `template_name='blog/login.html'`).

### `django_blog/settings.py`

The following settings were added to configure behavior for the built-in views:

```python
LOGIN_REDIRECT_URL = '/'  # Redirect on successful login
LOGOUT_REDIRECT_URL = '/' # Redirect on successful logout
LOGIN_URL = '/login/'     # Default URL to redirect unauthenticated users to