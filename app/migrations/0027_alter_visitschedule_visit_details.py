# Generated by Django 4.0.2 on 2022-03-13 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_visitdetails_visitschedule_visit_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitschedule',
            name='visit_details',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.visitdetails'),
        ),
    ]