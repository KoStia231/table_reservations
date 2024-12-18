from datetime import datetime, timedelta

from django.db.models import Q
from django.utils.timezone import make_aware
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView

from table_rezerv.forms import (
    ReservationCreateForm, TableFilterForm, ReservationChangeForm,
    ReservationCancelForm, ReservationConfirmForm
)
from table_rezerv.models import Table, Reservation
from users.views import MyLoginRequiredMixin
from table_rezerv.utils.utils import is_table_available


class TableView(MyLoginRequiredMixin, ListView):
    model = Table
    template_name = 'table_rezerv/list_table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TableFilterForm(self.request.GET or None)
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        filter_form = TableFilterForm(self.request.GET or None)

        if filter_form.is_valid():
            filter_date = filter_form.cleaned_data['date']
            filter_time = filter_form.cleaned_data['time']
            # Сохранение времени и даты из формы в request.session
            self.request.session['filter_date'] = str(filter_date)
            self.request.session['filter_time'] = str(filter_time)

            naive_filter_datetime = datetime.combine(filter_date, filter_time)
            filter_datetime = make_aware(naive_filter_datetime)
            # Исключение столиков с пересекающимися бронированиями
            queryset = queryset.filter(
                Q(status=Table.Status.FREE) |
                ~Q(
                    # Только активные брони
                    reservations__status__in=['confirmed', 'pending'],
                    # Совпадает дата
                    reservations__date=filter_date,
                    # Бронь началась до выбранного времени
                    reservations__time__lte=filter_datetime.time(),
                    # Бронь закончится позже выбранного времени
                    reservations__end_time__gt=filter_datetime
                )
            ).distinct()

        return queryset


class ReservationCreateView(MyLoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationCreateForm
    template_name = 'table_rezerv/object_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request  # Передача request.session
        kwargs['table_pk'] = self.kwargs['table_pk']
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Очистка данных из сессии при создании брони
        self.request.session.pop('filter_date', None)
        self.request.session.pop('filter_time', None)

        date, time = form.cleaned_data['date'], form.cleaned_data['time']
        duration = form.cleaned_data['duration']
        start_datetime = make_aware(datetime.combine(date, time))
        end_datetime = start_datetime + timedelta(hours=duration)
        table = Table.objects.get(id=self.kwargs['table_pk'])

        if start_datetime < make_aware(datetime.now()):
            form.add_error(None, 'Время или дата не может быть в прошлом')
            return self.form_invalid(form)

        # Проверка свободен ли столик в это время
        if is_table_available(table, date, start_datetime, end_datetime):
            form.add_error(None, 'Этот столик уже забронирован на выбранное время.')
            return self.form_invalid(form)
        reservation = form.save(commit=False)
        reservation.customer = self.request.user
        reservation.status = Reservation.Status.PENDING
        reservation.end_time = end_datetime
        reservation.save()
        table.status = Table.Status.RESERVED
        table.save()
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        return reverse('users:profile', args=[user.pk])


class ReservationBaseView(MyLoginRequiredMixin, UpdateView):
    model = Reservation
    template_name = 'table_rezerv/object_form.html'

    def get_success_url(self):
        user = self.request.user
        return reverse('users:profile', args=[user.pk])


class ReservationChangeView(ReservationBaseView):
    form_class = ReservationChangeForm

    def form_valid(self, form):
        reservation = form.save(commit=False)
        date, time = form.cleaned_data['date'], form.cleaned_data['time']
        duration = form.cleaned_data['duration']
        start_datetime = make_aware(datetime.combine(date, time))
        end_datetime = start_datetime + timedelta(hours=duration)
        table = reservation.table

        if start_datetime < make_aware(datetime.now()):
            form.add_error(None, 'Время или дата не может быть в прошлом')
            return self.form_invalid(form)

        # Проверка свободен ли столик в это время
        if is_table_available(table, date, start_datetime, end_datetime):
            form.add_error(None, 'Этот столик уже забронирован на выбранное время.')
            return self.form_invalid(form)

        reservation.end_time = end_datetime
        reservation.save()

        return super().form_valid(form)


class ReservationConfirmView(ReservationBaseView):
    form_class = ReservationConfirmForm

    def form_valid(self, form):
        reservation = form.save(commit=False)
        table = reservation.table
        table.status = table.Status.BUSY
        table.save()
        reservation.save()
        return super().form_valid(form)


class ReservationCancelView(ReservationBaseView):
    form_class = ReservationCancelForm

    def form_valid(self, form):
        reservation = form.save(commit=False)
        table = reservation.table
        table.status = table.Status.FREE
        table.save()
        reservation.save()
        return super().form_valid(form)
