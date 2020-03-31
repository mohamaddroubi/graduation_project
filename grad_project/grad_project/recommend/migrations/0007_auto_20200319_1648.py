# Generated by Django 2.2.10 on 2020-03-19 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recommend', '0006_auto_20200319_1440'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='ratings',
        ),
        migrations.CreateModel(
            name='ItemRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(blank=True, choices=[(1, 'Very Poor'), (2, 'Poor'), (3, 'Neutral'), (4, 'Good'), (5, 'Very Good')], null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommend.Item')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
