# Generated by Django 4.2.2 on 2024-11-27 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_sitetext_key'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feedback',
            options={'verbose_name': 'Обращение', 'verbose_name_plural': 'Обращения и системные уведомления "SYSTEM"'},
        ),
    ]
