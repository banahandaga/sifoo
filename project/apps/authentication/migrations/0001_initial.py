# Generated by Django 4.1 on 2024-03-02 23:35

import apps.authentication.models.profile
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupDetails',
            fields=[
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='groupdetails', serialize=False, to='auth.group')),
                ('alias', models.CharField(max_length=100, null=True)),
                ('description', models.TextField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nip', models.CharField(blank=True, max_length=20, null=True)),
                ('nidn', models.CharField(blank=True, max_length=50, null=True)),
                ('surelluar', models.CharField(blank=True, max_length=100, null=True)),
                ('nomorhp', models.CharField(blank=True, max_length=15, null=True)),
                ('is_dosen', models.IntegerField(blank=True, null=True)),
                ('home_id', models.CharField(blank=True, max_length=20, null=True)),
                ('homebase', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=apps.authentication.models.profile.path_image)),
                ('otp', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
