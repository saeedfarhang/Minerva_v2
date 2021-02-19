# Generated by Django 3.1.6 on 2021-02-14 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('avatar', models.FileField(default='avatars/default.jpg', upload_to='avatars/%Y/%m')),
                ('phone_number', models.CharField(blank=True, max_length=12, null=True, unique=True)),
                ('national_code', models.CharField(blank=True, max_length=12, null=True, unique=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('city', models.CharField(blank=True, choices=[('yazd', 'yazd'), ('tehran', 'tehran'), ('esfahan', 'esfahan')], default='tehran', max_length=12, null=True)),
                ('address', models.CharField(blank=True, max_length=112, null=True)),
                ('coins', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_master', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]