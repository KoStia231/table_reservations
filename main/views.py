import re

from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, TemplateView

from main.forms import FeedbackForm, FeedbackFormUserAuf
from main.models import (
    SiteImage, SiteText,
    Staff, Services, Feedback
)


class IndexView(CreateView):
    """Отображение главной страницы"""
    model = Feedback
    template_name = 'main/index.html'

    def get_form_class(self):
        """Разные формы авторизованным и не авторизованным пользователям"""
        if self.request.user.is_authenticated:
            return FeedbackFormUserAuf
        return FeedbackForm

    def get_form_kwargs(self):
        """Передаёт user в форму, только для авторизованных пользователей"""
        kwargs = super().get_form_kwargs()
        if self.request.user.is_authenticated:
            kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Обработка и сохранение формы с валидацией номера телефона"""
        if self.request.user.is_authenticated:
            return super().form_valid(form)
            # return redirect(self.get_success_url())
        else:
            if form.is_valid():
                feedback = form.save(commit=False)
                phone = form.cleaned_data.get('phone')
                regular = re.sub(r'\D', '', phone)
                if len(regular) != 10:
                    form.add_error('phone', 'Номер телефона должен содержать ровно 10 цифр.')
                    return super().form_invalid(form)
                formatted_phone = f"+7{regular}"
                feedback.phone = formatted_phone
                feedback.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_description'] = SiteText.objects.filter(key=SiteText.KeyChoices.MAIN_DESCRIPTION).first()
        context['main_contacts'] = SiteText.objects.filter(key=SiteText.KeyChoices.MAIN_CONTACTS).first()
        context['main_banner'] = SiteImage.objects.filter(key=SiteImage.KeyChoices.MAIN_BANNER).first()
        context['reservation_banner'] = SiteImage.objects.filter(key=SiteImage.KeyChoices.RESERVATION_BANNER).first()
        context['services'] = Services.objects.all()
        return context


class AboutView(TemplateView):
    """Отображение О нас страницы"""
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about_history'] = SiteText.objects.filter(key=SiteText.KeyChoices.ABOUT_HISTORY).first()
        context['about_mission'] = SiteText.objects.filter(key=SiteText.KeyChoices.ABOUT_MISSION).first()
        context['about_history_image'] = SiteImage.objects.filter(key=SiteImage.KeyChoices.ABOUT_HISTORY_IMAGE).first()
        context['staffs'] = Staff.objects.all()
        return context
