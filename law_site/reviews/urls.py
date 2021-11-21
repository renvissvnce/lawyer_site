from django.urls import path
from . import views


urlpatterns = [
    path('reviews', views.reviews, name='reviews'),
    path('register', views.register, name='reg'),
    path('login', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate')
]