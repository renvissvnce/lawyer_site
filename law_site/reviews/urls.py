from django.urls import path, include
from . import views


urlpatterns = [
    path('reviews', views.reviews, name='reviews'),

]