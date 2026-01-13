from django.urls import path
from . import views

#URLConfiguration
urlpatterns = [path('', views.home_screen),
               path('about/', views.about),
               path('contact/', views.contact)]
