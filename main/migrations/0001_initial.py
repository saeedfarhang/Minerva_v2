# Generated by Django 3.1.6 on 2021-02-18 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='Categories_thumbnails/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='tags_thumbnails/%Y/%m/%d')),
            ],
        ),
    ]
