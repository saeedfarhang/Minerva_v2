# Generated by Django 3.1.6 on 2021-02-18 18:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_auto_20210218_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
