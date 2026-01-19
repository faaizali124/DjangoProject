from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Post
from .forms import PostForm

def home_screen(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts':posts})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    
    return render(request, 'add_post.html', {'form' : form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, user = request.user, id=post_id)
    if(request.method == 'POST'):
        form = PostForm(request.POST, instance = post)
        if(form.is_valid()):
            form.save()
            return redirect('post_detail', post_id = post.id)
    else:
        form = PostForm(instance = post)
    
    return render(request, 'edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, user = request.user, id = post_id)
    if(request.method == 'POST'):
        post.delete()
        return redirect('home')
    
    return render(request, 'delete_post.html', {'post': post})

@login_required
def my_posts(request):
    posts = Post.objects.filter(user = request.user)
    return render(request, 'my_posts.html', {'posts': posts})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {'form': form})
