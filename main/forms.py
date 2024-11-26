from django import forms

from main.models import Feedback


class FeedbackFormUserAuf(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'phone', 'message', ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите ваше сообщение'}),
        }


class FeedbackForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=13,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш телефон',
            'pattern': r'\d{10}',  # Валидация через HTML5 pattern (только 10 цифр)
            'title': 'Номер телефона без +7 и без 8',
            'required': 'required',
        }),
    )

    class Meta:
        model = Feedback
        fields = ['name', 'email', 'phone', 'message', ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш телефон'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите ваше сообщение'}),
        }
