# Generated by Django 4.1.3 on 2022-11-25 20:49

import account.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('name', models.CharField(max_length=150)),
                ('is_active', models.BooleanField(default=False)),
                ('is_vendor', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_customer', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', account.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=150)),
                ('mobile', models.CharField(max_length=150)),
                ('brand_name', models.CharField(max_length=150)),
                ('profile_pic', models.ImageField(blank=True, default='avatars/avatar.jpg', upload_to='vendor/profile_pic')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vendor', to=settings.AUTH_USER_MODEL, verbose_name='Vendor')),
            ],
            options={
                'verbose_name': 'Vendor',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=150)),
                ('mobile', models.CharField(max_length=150)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL, verbose_name='Customer')),
            ],
            options={
                'verbose_name': 'Customer',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=150, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=150, verbose_name='last Name')),
                ('mobile', models.CharField(max_length=50, verbose_name='Phone Number')),
                ('postcode', models.CharField(max_length=50, verbose_name='Postcode')),
                ('address', models.CharField(max_length=255, verbose_name='Address')),
                ('town_city', models.CharField(max_length=150, verbose_name='Town/City')),
                ('state', models.CharField(max_length=150, verbose_name='State')),
                ('default', models.BooleanField(default=False, verbose_name='Default')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.customer', verbose_name='Customer')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
        ),
    ]