# Generated by Django 4.0.2 on 2022-03-06 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_availability', '0004_patient_age'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('centres', models.ManyToManyField(help_text='Select the AusCAT entres you wish to track in the dashboard', related_name='auscat_centres', to='data_availability.Centre', verbose_name='AusCAT Centres')),
            ],
        ),
    ]
