# Generated by Django 4.0.2 on 2022-03-05 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_familydetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familydetail',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app.patient'),
        ),
    ]
