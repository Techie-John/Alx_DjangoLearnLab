from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import CustomUserCreationForm, UserUpdateForm, CommentForm 
from django.db.models import Q 

# --- Task 0 Home View (Keep this) ---
def home_view(request):
    context = {
        'message': 'Welcome to the Django Blog!',
        'post_count': Post.objects.count(),
    }
    return render(request, 'blog/home.html', context)
# -----------------------------------


# Step 1: Registration View
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Automatically log in the user after registration
            messages.success(request, f'Account created for {user.username}!')
            return redirect('blog_home') # Redirect to home or another page
        else:
            # Add error message if form is invalid
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

# Step 4: Profile Management View
@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Error updating your profile.')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'blog/profile.html', {'form': form})



# READ: List All Posts (Accessible to all)
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # <app>/<model>_list.html
    context_object_name = 'posts' # Name of the queryset in the template
    ordering = ['-published_date']
    paginate_by = 5

# READ: View a Single Post (Accessible to all)
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

# CREATE: New Post (Requires login)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'tags'] # Uses default ModelForm fields
    template_name = 'blog/post_form.html'

    # Auto-set the author before saving the form
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# UPDATE: Edit Post (Requires login and must be the author)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'tags']
    template_name = 'blog/post_form.html'

    # Auto-set the author before saving (needed for validation, although author won't change)
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Permission check: Only author can edit
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# DELETE: Delete Post (Requires login and must be the author)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list') # Redirect to the post list after deletion

    # Permission check: Only author can delete
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
        
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the Comment form to the context
        context['comment_form'] = CommentForm()
        # Add the list of comments (fetched via related_name='comments')
        context['comments'] = self.object.comments.all() 
        return context

#  NEW COMMENT CREATE VIEW 
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html' # This template is only used if accessed directly

    # Set the author and post before saving the form
    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    # Success URL is defined on the model (get_absolute_url) 
    # which redirects back to the post detail page.

#  NEW COMMENT UPDATE VIEW 
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    # Permission check: Only the comment author can edit
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

#  NEW COMMENT DELETE VIEW 
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    # Permission check: Only the comment author can delete
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    # After deletion, redirect back to the post's detail page
    def get_success_url(self):
        post_pk = self.object.post.pk
        return reverse('post_detail', kwargs={'pk': post_pk})

def search_results_view(request):
    query = request.GET.get('q', '')
    results = Post.objects.none() # Initialize empty queryset

    if query:
        # 💥 Use Q objects for OR logic across multiple fields/models 💥
        # Filter by title, content (using icontains for case-insensitive lookup)
        # Filter by tags (using taggit's manager lookup)
        results = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) | 
            Q(tags__name__in=[query])
        ).distinct().order_by('-published_date')

    context = {
        'query': query,
        'posts': results,
    }
    return render(request, 'blog/search_results.html', context)


# 💥 Tag Filtering View Implementation 💥
def post_by_tag_view(request, tag_slug):
    # Fetch posts filtered by the given tag slug
    posts = Post.objects.filter(tags__slug__in=[tag_slug]).order_by('-published_date')
    tag_name = tag_slug.replace('-', ' ').title() # Simple conversion for display

    context = {
        'tag_name': tag_name,
        'posts': posts,
    }
    return render(request, 'blog/tag_posts.html', context)