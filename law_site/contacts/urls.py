from django.urls import path, include
from . import views


urlpatterns = [
    path('contacts', views.contacts, name='contacts'),
    #path('feedback', views.feedback, name='feedback'),
]