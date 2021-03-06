# Generated by Django 4.0.2 on 2022-03-01 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_patient_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='expired_time',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='facility',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='app.facility'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='patient',
            name='ward',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='app.ward'),
            preserve_default=False,
        ),
    ]
