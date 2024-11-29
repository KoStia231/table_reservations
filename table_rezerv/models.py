from django.db import models

from users.models import NULLABLE
from users.models import User


class Table(models.Model):
    class Status(models.TextChoices):
        FREE = 'F', 'Свободный'
        RESERVED = 'R', 'Зарезервирован'
        BUSY = 'B', 'Занят'

    status = models.CharField(
        choices=Status.choices, max_length=1,
        default=Status.FREE, verbose_name='Статус резервации'
    )
    seats = models.PositiveSmallIntegerField(verbose_name='Количество мест')
    number = models.PositiveSmallIntegerField(verbose_name='Номер столика')
    description = models.TextField(max_length=255, verbose_name='Описание/расположение')
    image = models.ImageField(upload_to='tables/', verbose_name='фото столика', **NULLABLE)

    def __str__(self):
        return f'Столик №{self.number}'

    @property
    def detailed_info(self):
        return f'Столик №{self.number} ({self.get_status_display()}), {self.seats} мест'

    class Meta:
        verbose_name = 'столик'
        verbose_name_plural = 'столики'


class Reservation(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = 'confirmed', 'Подтверждена'
        CANCELLED = 'cancelled', 'Отменена'
        COMPLETED = 'completed', 'Завершена'
        PENDING = 'pending', 'Ожидает подтверждения'

    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="reservations", verbose_name="Столик")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations", verbose_name="Клиент")
    date = models.DateField(verbose_name="Дата бронирования")
    time = models.TimeField(verbose_name="Время бронирования")
    duration = models.PositiveIntegerField(verbose_name="Продолжительность (в часах)", default=1)
    end_time = models.DateTimeField(verbose_name="Время окончания брони", )
    status = models.CharField(max_length=10, choices=Status.choices, default='pending', verbose_name="Статус брони")

    def __str__(self):
        return f"Бронь: {self.table}, дата: ({self.date}, время: {self.time})"

    @property
    def detailed_info(self):
        return (f"({self.get_status_display()})  Бронь: {self.table} для {self.customer}, "
                f"(дата:{self.date}, время: {self.time}), "
                f"продолжительность {self.duration} час")

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'
