# Generated by Django 4.0.2 on 2022-03-06 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_availability', '0003_patient_centre_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='age',
            field=models.IntegerField(blank=True, help_text='Age', null=True),
        ),
    ]
