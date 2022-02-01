from .models import Feedback
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ('fio', 'phone', 'mail', 'topic', 'full_text')

        widgets = {
            'fio': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше ФИО',
            }),
            'phone': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш телефон',
            }),
            'mail': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваша электронная почта',
            }),
            'topic': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Тема вашего обращения',
            }),
            'full_text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Опишите вашу проблему',
            }),
            'date': DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше ФИО',
            })

        }
