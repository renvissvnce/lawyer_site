from django.shortcuts import render, redirect, reverse
from .forms import ReviewsForm
from .models import Reviews, Acc
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def reviews(request):
    if request.method == "GET":
        p = Reviews.objects.all()
        acc = Acc.objects.all()
        form = ReviewsForm(request.POST)
        return render(request, 'reviews/reviews.html', {'p': p, 'form': form, 'name' : request.user.username })

    elif request.method == 'POST':
        form = ReviewsForm(request.POST)
        messages.success(request, 'Отзыв успешно добавлен!')
        if form.is_valid():
            form.save()
            return redirect('reviews')
        else:
            messages.success(request, 'Отзыв не был добавлен. Попытайтесь еще раз.')


def register(request):
    if request.method == "POST":
        context = {'has_error': False, 'data': request.POST}
        phone = request.POST.get('phone')
        username = request.POST.get('username')
        fio = request.POST.get('fio')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if len(password) < 6:
            messages.add_message(request, messages.ERROR,
                                 'Пароль должен быть больше 6 символов')
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
                                 'Логин уже используется, пожалуйста, выберите другой')
            context['has_error'] = True

            return render(request, 'reviews/register.html', context, status=409)
        if context['has_error']:
            return render(request, 'reviews/register.html', context)

        user = Acc.objects.create_user(username=username, fio=fio, phone=phone)
        user.set_password(password)
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Аккаунт создан!')
        return redirect('login')


    return render(request, 'reviews/register.html')


def login_user(request):
    if request.method == 'POST':
        context = {'data': request.POST}
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if not user:
            messages.add_message(request, messages.ERROR, 'Неправильно введен логин или пароль')

            return render(request, 'reviews/login.html', context, status=401)

        login(request, user)
        return redirect('reviews')

    return render(request, 'reviews/login.html')



def logout_user(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Вы вышли со своей учетной записи.')
    return redirect(reverse('login'))