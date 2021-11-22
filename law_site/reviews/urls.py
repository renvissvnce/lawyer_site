from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('reviews', views.reviews, name='reviews'),
    path('register', views.register, name='reg'),
    path('login', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('activate-user/<uidb64>/<token>',views.activate_user, name='activate'),

    path('reset_password/', views.password_reset_request, name="password_reset", ),


    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name='reviews/password_reset.html'),
    #      name='password_reset'),


    path('reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(template_name="reviews/password_reset_sent.html"),
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="reviews/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name="reviews/password_reset_done.html"),
        name="password_reset_complete"),
]