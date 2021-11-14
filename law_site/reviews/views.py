from django.shortcuts import render, redirect
from .forms import ReviewsForm
from .models import Reviews


def reviews(request):
    if request.method == "GET":
        p = Reviews.objects.all()
        form = ReviewsForm(request.POST)
        return render(request, 'reviews.html', {'p': p, 'form': form})

    elif request.method == 'POST':
        form = ReviewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reviews')

