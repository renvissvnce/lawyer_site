from django.urls import path, include
from . import views


urlpatterns = [
    path('prices', views.prices, name='prices'),

]
