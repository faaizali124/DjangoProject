from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Post

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