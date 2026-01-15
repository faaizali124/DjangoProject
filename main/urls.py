from django.urls import path
from . import views

#URLConfiguration
urlpatterns = [path('', views.home_screen, name = 'home'),
               path('about/', views.about, name = 'about'),
               path('contact/', views.contact, name = 'contact'),
               path('post/<int:post_id>/', views.post_detail, name = 'post_detail'),
               path('add-post/', views.add_post, name = 'add_post')]
