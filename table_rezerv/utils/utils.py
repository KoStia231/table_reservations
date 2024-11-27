from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from main.models import Feedback


def send_email_reservation_to_cancelled(user_email, table, data, time):
    try:
        send_mail(
            subject=f'Информация о бронировании',
            message=f'Ваша бронь столика {table} на дату: {data}, время {time} была автоматически отменена',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user_email],
        )
    except Exception as e:
        Feedback.objects.create(
            name='SYSTEM',
            email=EMAIL_HOST_USER,
            phone='',
            message=f'Ошибка при отправке письма о бронировании для столика {table} на {data} в {time}:\n {str(e)}'
        )
        print(e)
