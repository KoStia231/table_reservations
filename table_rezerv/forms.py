from datetime import datetime

from django import forms

from .models import Reservation, Table


class ReservationCreateForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['table', 'date', 'time', 'duration', 'status', 'customer']
        widgets = {
            'table': forms.Select(attrs={'class': 'form-control', 'readonly': True}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control', 'readonly': True}),
            'customer': forms.Select(attrs={'class': 'form-control', 'readonly': True}),
        }

    def __init__(self, *args, **kwargs):
        table_pk = kwargs.pop('table_pk', None)
        user = kwargs.pop('user', None)
        super(ReservationCreateForm, self).__init__(*args, **kwargs)
        if table_pk:
            self.fields['table'].queryset = Table.objects.filter(pk=table_pk)
            self.fields['table'].initial = Table.objects.get(pk=table_pk)

        if user and user.is_authenticated:
            self.fields['customer'].initial = user
            self.fields['status'].initial = Reservation.Status.PENDING

        self.fields['date'].initial = datetime.now().date()
        self.fields['time'].initial = datetime.now().time()
        self.fields['duration'].initial = 1


class ReservationChangeForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['table', 'date', 'time', 'duration', ]
        widgets = {
            'table': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
        }


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


class TableFilterForm(forms.Form):
    date = forms.DateField(
        initial=datetime.now(),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'min': datetime.today().date()}),
        required=True,
        label='Выберите дату'
    )

    time = forms.TimeField(
        initial=datetime.now().strftime('%H:%M'),
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'min': datetime.now().strftime('%H:%M')}),
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
        now = datetime.now()
        if selected_time < now.time():
            raise forms.ValidationError('Время не может быть в прошлом.')
        return selected_time
