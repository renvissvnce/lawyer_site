from .models import Reviews, RATE_CHOICES, Acc
from datetime import datetime
from django.forms import ModelForm, TextInput, DateTimeField, Textarea, ChoiceField, Select, CharField


class ReviewsForm(ModelForm):
    class Meta:
        model = Reviews
        fields = ('__all__')


    fio = Acc.fio
    #CharField(required=True,
    #                   widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше ФИО'}))
    phone = CharField(required=True,
                      widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш телефон'}))
    case_number = CharField(required=True,
                            widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер обращения'}))
    topic = CharField(required=True,
                      widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите тему обращения'}))
    rate = ChoiceField(choices=RATE_CHOICES, widget=Select(), required=True)
    full_text = CharField(widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите текст'}),
                          required=False)
    date = DateTimeField(initial=datetime.utcnow(), required=False)



    # widgets = {
    #     'fio': TextInput(attrs={
    #         'class': 'form-control',
    #         'value': 'request.fio'
    #     })}
    #     'phone': TextInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Ваш телефон'
    #     }),
    #     'case_number': TextInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Ваша электронная почта'
    #     }),
    #     'topic': TextInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Тема вашего обращения'
    #     }),
    #     'full_text': Textarea(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Опишите вашу проблему'
    #     }),
    #     'date': DateTimeField(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Ваше ФИО'
    #     })
    #
    # }