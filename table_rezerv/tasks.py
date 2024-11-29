from datetime import datetime

from celery import shared_task
from django.utils.timezone import make_aware

from table_rezerv.models import Reservation, Table
from table_rezerv.utils.utils import send_email_reservation_to_cancelled


@shared_task
def check_reservations():
    now = make_aware(datetime.now())
    reservations = Reservation.objects.exclude(status__in=['cancelled', 'completed'])
    for reservation in reservations:
        end_time = reservation.end_time
        # Если время завершения прошло или равно текущему времени
        if end_time <= now:
            reservation.status = Reservation.Status.COMPLETED
            reservation.save()
            table = reservation.table
            table.status = Table.Status.FREE
            table.save()
            # Отправка письма и если ошибка отчет в базе с пометкой SYSTEM
            send_email_reservation_to_cancelled.delay(
                user_email=reservation.customer.email,
                phone=reservation.customer.phone,
                table=table,
                data=reservation.date,
                time=reservation.time
            )
