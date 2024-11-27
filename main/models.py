from django.db import models

from users.models import NULLABLE


class SiteText(models.Model):
    class KeyChoices(models.TextChoices):
        MAIN_DESCRIPTION = "main_description", "Описание ресторана (Главная)"
        MAIN_CONTACTS = "main_contacts", "Контактная информация (Главная)"
        ABOUT_HISTORY = "about_history", "История ресторана (О ресторане)"
        ABOUT_MISSION = "about_mission", "Миссия и ценности (О ресторане)"
        SITE_TITLE = "site_title", "Название сайта"

    key = models.CharField(
        max_length=50,
        unique=True,
        choices=KeyChoices.choices,
        verbose_name="Ключ текста"
    )
    value = models.TextField(verbose_name="Текст основной")
    value_1 = models.TextField(verbose_name="Текст 1", **NULLABLE)
    value_2 = models.TextField(verbose_name="Текст 2", **NULLABLE)
    value_3 = models.TextField(verbose_name="Текст 3", **NULLABLE)
    description = models.CharField(max_length=255, verbose_name="Описание", **NULLABLE)

    def __str__(self):
        return f"{self.key}"

    class Meta:
        verbose_name = "Текст сайта"
        verbose_name_plural = "Тексты сайта"


class SiteImage(models.Model):
    class KeyChoices(models.TextChoices):
        MAIN_BANNER = "main_banner", "Баннер (Главная)"
        ABOUT_HISTORY_IMAGE = "about_history_image", "История ресторана (О ресторане)"
        RESERVATION_BANNER = "reservation_banner", "Баннер страницы бронирования"

    key = models.CharField(
        max_length=50,
        unique=True,
        choices=KeyChoices.choices,
        verbose_name="Ключ изображения"
    )
    image = models.ImageField(upload_to="site_images/", verbose_name="Изображение основное")
    image_1 = models.ImageField(upload_to="site_images/", verbose_name="Изображение 1", **NULLABLE)
    image_2 = models.ImageField(upload_to="site_images/", verbose_name="Изображение 2", **NULLABLE)
    image_3 = models.ImageField(upload_to="site_images/", verbose_name="Изображение 3", **NULLABLE)
    description = models.CharField(max_length=255, verbose_name="Описание", **NULLABLE)

    def __str__(self):
        return f"{self.key}"

    class Meta:
        verbose_name = "Изображение сайта"
        verbose_name_plural = "Изображения сайта"


class Staff(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя Фамилия")
    image = models.ImageField(upload_to="site_images/staff", verbose_name="Картинка")
    job_title = models.CharField(max_length=100, verbose_name="Должность")
    description = models.CharField(max_length=100, verbose_name="Описание")

    def __str__(self):
        return f"{self.name} - {self.job_title}"

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"


class Services(models.Model):
    image = models.ImageField(upload_to="site_images/services", verbose_name="Картинка")
    description = models.CharField(max_length=100, verbose_name="Описание")
    title = models.CharField(max_length=100, verbose_name="Название")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class Feedback(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=13, verbose_name="Телефон")
    message = models.TextField(verbose_name="Сообщение")

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения и системные уведомления \"SYSTEM\""
