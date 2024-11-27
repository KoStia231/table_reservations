# Generated by Django 4.2.2 on 2024-11-26 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата бронирования')),
                ('time', models.TimeField(verbose_name='Время бронирования')),
                ('duration', models.PositiveIntegerField(default=1, verbose_name='Продолжительность (в часах)')),
                ('status', models.CharField(choices=[('confirmed', 'Подтверждена'), ('cancelled', 'Отменена'), ('completed', 'Завершена'), ('pending', 'Ожидает подтверждения')], default='pending', max_length=10, verbose_name='Статус брони')),
            ],
            options={
                'verbose_name': 'бронь',
                'verbose_name_plural': 'брони',
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('F', 'Свободный'), ('R', 'Зарезервирован'), ('B', 'Занят')], default='F', max_length=1, verbose_name='Статус резервации')),
                ('seats', models.PositiveSmallIntegerField(verbose_name='Количество мест')),
                ('number', models.PositiveSmallIntegerField(verbose_name='Номер столика')),
                ('description', models.TextField(max_length=255, verbose_name='Описание/расположение')),
                ('image', models.ImageField(blank=True, null=True, upload_to='tables/', verbose_name='фото столика')),
            ],
            options={
                'verbose_name': 'столик',
                'verbose_name_plural': 'столики',
            },
        ),
    ]