from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from users.models import User


class CustomFormMixin:
    """Стилизация внешнего вида формы"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(CustomFormMixin, UserCreationForm):
    # Наследуемся от специальной формы UserCreationForm из модуля auth
    phone = forms.CharField(
        max_length=13,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'pattern': r'\d{10}',  # Валидация через HTML5 pattern (только 10 цифр)
            'title': 'Номер телефона без +7 и без 8',
            'required': 'required',
        }),
        label='Номер телефона'
    )

    class Meta:
        model = User
        # Указываем новую кастомную модель
        fields = ('name', 'phone', 'email', 'password1', 'password2')
        # Меняем поля, так как исходная форма UserCreationForm
        # ссылается на поле username


class UserLoginForm(CustomFormMixin, AuthenticationForm):
    class Meta:
        model = User
        fields = ('email', 'password')
