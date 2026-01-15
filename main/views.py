from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
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

def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    
    return render(request, 'add_post.html', {'form' : form})

def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if(request.method == 'POST'):
        form = PostForm(request.POST, instance = post)
        if(form.is_valid()):
            form.save()
            return redirect('post_detail', post_id = post.id)
    else:
        form = PostForm(instance = post)
    
    return render(request, 'edit_post.html', {'form': form, 'post': post})

def delete_post(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    if(request.method == 'POST'):
        post.delete()
        return redirect('home')
    
    return render(request, 'delete_post.html', {'post': post})

    