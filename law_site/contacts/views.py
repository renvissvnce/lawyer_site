from django.shortcuts import render,redirect
from .forms import FeedbackForm


#def contacts(request):
    #return render(request, 'contacts/contacts2.html')


def contacts(request):
    error= ''
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contacts')
        else:
            error = 'Форма была неверной'
    form = FeedbackForm()

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'contacts/contacts.html', data)