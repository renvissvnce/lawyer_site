from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views.generic import FormView

from .forms import ReviewsForm
from .models import Reviews, Acc
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def reviews(request):
    if request.method == "GET":
        p = Reviews.objects.all()
        form = ReviewsForm(request.POST)
        return render(request, 'reviews/reviews.html', {'p': p, 'form': form, 'name': request.user})

    elif request.method == 'POST':
        form = ReviewsForm(request.POST)
        messages.success(request, 'Отзыв успешно добавлен!')
        if form.is_valid():
            form.save(request.user)
            return redirect('reviews')
        # form.save(request.user.fio)
        # if form.is_valid():
        #     form.fio = Acc.objects.get(pk=request.user.id)
        #     form.save()
        #     return redirect('reviews')

    else:
        messages.success(request, 'Отзыв не был добавлен. Попытайтесь еще раз.')


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Подтвердите ваш аккаунт'
    email_body = render_to_string('reviews/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_HOST_USER,
                         to=[user.email]
                         )
    EmailThread(email).start()


def send_reset_password(user, request):
    current_site = get_current_site(request)
    email_subject = 'Сброс пароля'
    email_body = render_to_string('reviews/password_reset_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_HOST_USER,
                         to=[user.email]
                         )

    email.send()
    EmailThread(email).start()


def register(request):
    if request.method == "POST":
        context = {'has_error': False, 'data': request.POST}
        phone = request.POST.get('phone')
        username = request.POST.get('username')
        #username = request.POST.get('username')
        fio = request.POST.get('fio')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if len(password) < 8:
            messages.add_message(request, messages.ERROR,
                                 'Пароль должен быть больше 8 символов')
            context['has_error'] = True

        if password != password2:
            messages.add_message(request, messages.ERROR,
                                 'Пароли не совпадают')
            context['has_error'] = True

        if not username:
            messages.add_message(request, messages.ERROR,
                                 'Введите логин')
            context['has_error'] = True

        if Acc.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR,
                                 'Никнейм уже занят, выберите другой.')
            context['has_error'] = True

            return render(request, 'reviews/register.html', context, status=409)
        if context['has_error']:
            return render(request, 'reviews/register.html', context)
        if Acc.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR,
                                 'Почта уже используется, введите другую.')
            context['has_error'] = True

            return render(request, 'reviews/register.html', context, status=409)

        user = Acc.objects.create_user(username=username, fio=fio, phone=phone, email=email)
        user.set_password(password)
        user.save()

        send_activation_email(user, request)
        messages.add_message(request, messages.SUCCESS,
                             'Аккаунт создан, осталось только подтвердить!')
        return redirect('login')

    return render(request, 'reviews/register.html')


def login_user(request):
    if request.method == 'POST':
        context = {'data': request.POST}
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user and not user.is_email_verified:
            messages.add_message(request, messages.ERROR, 'Подтвердите аккаунт, письмо было отправлено на вашу почту')

            return render(request, 'reviews/login.html', context, status=401)

        if not user:
            messages.add_message(request, messages.ERROR, 'Неправильно введен логин или пароль')

            return render(request, 'reviews/login.html', context, status=401)

        login(request, user)
        return redirect('reviews')

    return render(request, 'reviews/login.html')


def logout_user(request):
    logout(request)

    messages.add_message(request, messages.SUCCESS,
                         'Вы вышли со своей учетной записи.')

    return redirect(reverse('login'))


def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))

        user = Acc.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS, 'Почта была подтверждена!')

        return redirect(reverse('login'))

    return render(request, 'reviews/register.html')


def password_reset_request(request):
    if request.method == 'POST':
        current_site = get_current_site(request)
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            data = password_form.cleaned_data['email']
            user_email = Acc.objects.filter(Q(email=data))
            if user_email.exists():
                for user in user_email:
                    email_subject = 'Сброс пароля на сайте advokat-bekker.com'
                    email_template_name = render_to_string('reviews/password_reset_email.html',{
                        'domain': current_site,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'user': user,
                        'protocol': 'http'
                    })

                    email = EmailMessage(subject=email_subject, body=email_template_name,
                                         from_email=settings.EMAIL_HOST_USER, to=[user.email])
                    try:
                        EmailThread(email).start()
                        messages.add_message(request, messages.SUCCESS, 'Письмо было отправлено')
                    except:
                        return HttpResponse('Invalid')

                    return redirect('password_reset_done')
    else:
        password_form = PasswordResetForm()
    context = {
        'password_form': password_form,
    }

    return render(request, 'reviews/password_reset.html', context)



