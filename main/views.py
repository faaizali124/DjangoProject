from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import Post
from .forms import PostForm, SignUpForm

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
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            activation_link = request.build_absolute_uri(
                reverse('activate', kwargs={'uidb64': uid, 'token': token})
            )
            
            subject = 'Activate your account'
            text_content = f'''Please click the link to activate your account: {activation_link}'''
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            html_content=f'''<p>Please click the link to activate your account:</p>
            <a href="{activation_link}" style = "color: #1a73e8">Activate Your Account</a>'''
            email = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            recipient_list
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

            return redirect('verification_pending', uidb64 = uid)
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})

def verification_pending(request, uidb64):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
    if(request.method == 'POST'):
        if user is not None:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = request.build_absolute_uri(
                reverse('activate', kwargs={'uidb64': uid, 'token': token})
            )
            
            subject = 'Activate your account'
            text_content = f'''Please click the link to activate your account: {activation_link}'''
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            html_content=f'''<p>Please click the link to activate your account:</p>
            <a href="{activation_link}" style = "color: #1a73e8">Activate Your Account</a>'''
            email = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            recipient_list
            )

            email.attach_alternative(html_content, "text/html")
            email.send()
            return render(request, 'verification_pending.html', {'user': user})
    
    else:
        return render(request, 'verification_pending.html', {'user': user})

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user.is_active == False:
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            return HttpResponse('Activation link is invalid')
    else:
        return HttpResponse('Account already activated')