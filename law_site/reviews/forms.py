from .models import Reviews, RATE_CHOICES, Acc
from datetime import datetime
from django.forms import ModelForm, TextInput, DateTimeField, Textarea, ChoiceField, Select, CharField, PasswordInput, ValidationError, Form


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


class SetPasswordForm(Form):

    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    new_password1 = CharField(label=("New password"),
                                    widget=PasswordInput)
    new_password2 = CharField(label=("New password confirmation"),
                                    widget=PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2