# Generated by Django 3.1.6 on 2021-02-14 19:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20210214_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
