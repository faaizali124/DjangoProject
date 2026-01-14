from django.urls import path
from . import views

#URLConfiguration
urlpatterns = [path('', views.home_screen),
               path('about/', views.about),
               path('contact/', views.contact),
               path('post/<int:post_id>/', views.post_detail, name = 'post_detail')]
