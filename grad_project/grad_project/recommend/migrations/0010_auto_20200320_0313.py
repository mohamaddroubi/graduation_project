# Generated by Django 2.2.10 on 2020-03-20 01:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0009_auto_20200320_0110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='users_interseted',
            field=models.ManyToManyField(blank=True, related_name='interested', related_query_name='users_interested', to=settings.AUTH_USER_MODEL),
        ),
    ]
