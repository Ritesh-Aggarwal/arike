# Generated by Django 4.0.2 on 2022-03-13 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_alter_visitschedule_visit_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitschedule',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.patient'),
        ),
    ]
