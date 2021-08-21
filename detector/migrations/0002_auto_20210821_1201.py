# Generated by Django 3.2.6 on 2021-08-21 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detector', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='device_id',
            field=models.CharField(help_text='A random device identifier', max_length=10),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='measurement_data',
            field=models.JSONField(help_text='Measurement data in JSON'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='mode',
            field=models.TextField(help_text='Data collection mode (for selecting analysis)'),
        ),
    ]
