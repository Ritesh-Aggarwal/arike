# Generated by Django 4.0.2 on 2022-03-13 08:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_visitschedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitschedule',
            name='scheduled_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]