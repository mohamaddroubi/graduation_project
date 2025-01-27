# Generated by Django 2.2.10 on 2020-03-07 09:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('brand', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=1)),
                ('description', models.TextField()),
                ('category', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='')),
                ('users_interseted', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
