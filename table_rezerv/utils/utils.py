from django.core.mail import send_mail
import smtplib
from celery import shared_task
from django.db.models import Q
from config.settings import EMAIL_HOST_USER
from main.models import Feedback
from table_rezerv.models import Reservation, Table


@shared_task
def send_email_reservation_to_cancelled(user_email, phone, table_pk, data, time):
    """
        Отправляет уведомление на электронную почту пользователя о том, что его бронь была отменена.
        В случае ошибки при отправке письма, создается запись в таблице Feedback с информацией об ошибке.
        :param user_email: Электронная почта пользователя, которому отправляется уведомление
        :param phone: Номер телефона пользователя
        :param table_pk: Table.pk
        :param data: Дата брони
        :param time: Время брони
        """
    table = Table.objects.get(pk=table_pk)
    try:
        send_mail(
            subject=f'Информация о бронировании',
            message=f'Ваша бронь столика {table} на дату: {data}, время {time} была автоматически отменена',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user_email],
        )
    except smtplib.SMTPException as e:
        Feedback.objects.create(
            name='SYSTEM',
            email=user_email,
            phone=phone or 'Не указан',
            message=f'Ошибка при отправке письма о бронировании для столика {table} на {data} в {time}'
                    f'для пользователя {user_email}:\n {str(e)}'
        )
        print(e)


def is_table_available(table, date, start_datetime, end_datetime) -> bool:
    """
    Проверяет, доступен ли столик для бронирования на выбранное время и дату.
    :param table: Объект столика
    :param date: Дата бронирования
    :param start_datetime: Начало бронирования
    :param end_datetime: Конец бронирования
    :return: True, если столик занят, иначе False
    """
    conflicting_reservations = Reservation.objects.filter(
        Q(table=table) &
        Q(status__in=['confirmed', 'pending']) &  # Только брони с подтвержденным или ожидающим статусом
        Q(date=date) &  # Совпадает дата
        (
            # - Время начала новой брони меньше, чем время окончания существующей брони
            # - Время окончания новой брони больше, чем время начала существующей брони
            (Q(time__lt=end_datetime.time()) & Q(end_time__gt=start_datetime))
        )
    )

    return conflicting_reservations.exists()  # Если есть пересечение, то True
