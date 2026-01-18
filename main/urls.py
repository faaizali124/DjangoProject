from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

#URLConfiguration
urlpatterns = [path('', views.home_screen, name = 'home'),
               path('about/', views.about, name = 'about'),
               path('contact/', views.contact, name = 'contact'),
               path('post/<int:post_id>/', views.post_detail, name = 'post_detail'),
               path('add-post/', views.add_post, name = 'add_post'),
               path('post/<int:post_id>/edit/', views.edit_post, name = 'edit_post'),
               path('post/<int:post_id>/delete/', views.delete_post, name = 'delete_post'),
               path('my_posts/', views.my_posts, name = 'my_posts'),
               path('login/', auth_views.LoginView.as_view(), name = 'login'),
               path('logout/', auth_views.LogoutView.as_view(next_page='/'), name = 'logout'),
               path('accounts/profile/', views.home_screen, name='profile')
               ]
