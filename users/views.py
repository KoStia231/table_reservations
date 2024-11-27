import random
import secrets
import string
import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView

from config.settings import EMAIL_HOST_USER
from table_rezerv.models import Reservation
from users.forms import UserLoginForm
from users.forms import UserRegisterForm
from users.models import User


class MyLoginRequiredMixin(LoginRequiredMixin):
    """Миксин для всех страниц, которые требуют авторизации"""
    login_url = 'users:login'
    redirect_field_name = "redirect_to"


class UserLoginView(LoginView):
    """Страничка входа"""
    template_name = 'users/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True  # авторизовать пользователя при успешном входе

    def get_success_url(self):
        user_pk = self.request.user.pk
        return reverse('users:profile', kwargs={'pk': user_pk})


class UserRegisterView(CreateView):
    """Страничка регистрации нового пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/registr.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Отправка пользователю письма с подтверждением регистрации"""
        user = form.save()
        phone = form.cleaned_data.get('phone')
        regular = re.sub(r'\D', '', phone)
        if len(regular) != 10:
            form.add_error('phone', 'Номер телефона должен содержать ровно 10 цифр.')
            return super().form_invalid(form)
        formatted_phone = f"+7{regular}"
        user.phone = formatted_phone
        user.is_active = False
        token_auf = secrets.token_hex(16)  # генерит токен
        user.token_auf = token_auf
        user.save()
        host = self.request.get_host()  # это получение хоста
        url = f'http://{host}/verify/{token_auf}'
        send_mail(
            subject=f'Подтверждение регистрации',
            message=f'Для подтверждения регистрации перейдите по ссылке: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def verify_mail(request, token_auf):
    """Подтверждение регистрации переход по ссылке из письма и редирект на страницу входа"""
    user = get_object_or_404(User, token_auf=token_auf)  # получить пользователя токен
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


def reset_password(request):
    """Сброс пароля и отправка письма """

    if request.method == 'POST':
        email = request.POST.get('email')

        if not User.objects.filter(email=email).exists():
            # это чтобы яндекс не пытался отправить письмо на не существующий адрес
            return render(request, template_name='users/reset_password.html')
        else:
            user = get_object_or_404(User, email=email)
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))  # генерит новый пароль
            user.set_password(new_password)
            user.save()
            send_mail(
                subject=f'Сброс пароля',
                message=f'Ваш новый пароль: {new_password}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[email],
            )
        return redirect(reverse('users:login'))

    return render(request, template_name='users/reset_password.html')


class UserProfileView(MyLoginRequiredMixin, DetailView):
    """Страничка просмотра профиля пользователя"""
    model = User
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservations'] = Reservation.objects.filter(customer=self.request.user)
        return context
