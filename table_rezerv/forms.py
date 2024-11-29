from datetime import datetime, timedelta

from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User
from .models import Reservation, Table


class TableFilterForm(forms.Form):
    date = forms.DateField(
        initial=datetime.now(),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'min': datetime.today().date()}),
        required=True,
        label='Выберите дату'
    )

    time = forms.TimeField(
        initial=datetime.now().strftime('%H:%M'),
        widget=forms.TimeInput(
            attrs={'type': 'time', 'class': 'form-control', 'init': datetime.now().strftime('%H:%M')}),
        required=True,
        label='Выберите время'
    )

    def clean_date(self):
        selected_date = self.cleaned_data['date']
        if selected_date < datetime.today().date():
            raise forms.ValidationError('Дата не может быть в прошлом.')
        return selected_date

    def clean_time(self):
        selected_time = self.cleaned_data['time']
        selected_date = self.cleaned_data['date']
        now = datetime.now()
        if selected_date == now.date():
            if selected_time < now.time():
                raise forms.ValidationError('Время не может быть в прошлом относительно текущего времени.')

        return selected_time


class ReservationCreateForm(TableFilterForm, forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['table', 'date', 'time', 'duration', 'status', 'customer']
        widgets = {
            'table': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'customer': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        table_pk = kwargs.pop('table_pk', None)
        user = kwargs.pop('user', None)
        request = kwargs.pop('request', None)
        super(ReservationCreateForm, self).__init__(*args, **kwargs)
        if table_pk:
            self.fields['table'].queryset = Table.objects.filter(pk=table_pk)
            self.fields['table'].initial = Table.objects.get(pk=table_pk)

        if user and user.is_authenticated:
            pk = user.pk
            self.fields['customer'].queryset = User.objects.filter(pk=pk)
            self.fields['customer'].initial = user
            self.fields['status'].choices = [(Reservation.Status.PENDING, 'Ожидает подтверждения')]

        # Автозаполнение формы на основе фильтра из сессии
        if request:
            filter_date = request.session.get('filter_date')
            filter_time = request.session.get('filter_time')
            self.fields['date'].initial = filter_date or datetime.now().date()
            self.fields['time'].initial = filter_time or (datetime.now() + timedelta(minutes=2)).strftime('%H:%M')
        else:
            self.fields['date'].initial = datetime.now().date()
            self.fields['time'].initial = (datetime.now() + timedelta(minutes=2)).strftime('%H:%M')

        self.fields['duration'].validators.append(MinValueValidator(1))
        self.fields['duration'].validators.append(MaxValueValidator(24))
        self.fields['duration'].initial = 1


class ReservationChangeForm(TableFilterForm, forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['table', 'date', 'time', 'duration', ]
        widgets = {
            'table': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ReservationChangeForm, self).__init__(*args, **kwargs)
        self.fields['duration'].validators.append(MinValueValidator(1))
        self.fields['duration'].validators.append(MaxValueValidator(24))


class ReservationConfirmForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('confirmed', 'Подтверждена'),
    ]

    class Meta:
        model = Reservation
        fields = ['status']

    status = forms.ChoiceField(choices=STATUS_CHOICES, initial='confirmed', label='Статус бронирования')


class ReservationCancelForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('cancelled', 'Отменена'),
    ]

    class Meta:
        model = Reservation
        fields = ['status']

    status = forms.ChoiceField(choices=STATUS_CHOICES, initial='cancelled', label='Статус бронирования')
