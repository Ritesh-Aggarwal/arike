# Generated by Django 4.0.2 on 2022-03-13 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_treatmentnotes_visitschedule_treatment_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treatmentnotes',
            name='visit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.visitschedule'),
        ),
    ]
