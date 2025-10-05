from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    # ... (Keep existing Post CBV imports) ...
    PostListView,      
    PostDetailView,    
    PostCreateView,    
    PostUpdateView,    
    PostDeleteView,
    CommentCreateView, #  NEW IMPORT 
    CommentUpdateView, #  NEW IMPORT 
    CommentDeleteView, #  NEW IMPORT 
    post_by_tag_view,
    search_results_view,
)

urlpatterns = [
    # ... (Keep existing Post CRUD URLs) ...
    path('', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/new/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    #  Step 5: Comment URLs 
    # Create (uses post pk for context, hence <int:pk>)
    path('posts/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment_create'),
    # Update/Delete (uses comment pk for identity)
    path('comments/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_update'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),

    # ... (Keep existing Auth URLs) ...
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('search/', search_results_view, name='search_results'),
    path('tags/<str:tag_slug>/', post_by_tag_view, name='posts_by_tag'),
]