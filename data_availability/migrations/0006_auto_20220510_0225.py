# Generated by Django 3.2.13 on 2022-05-10 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_availability', '0005_config'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='db_name',
            field=models.CharField(help_text='Database name', max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='config',
            name='db_password',
            field=models.CharField(help_text='Database password', max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='config',
            name='db_servername',
            field=models.CharField(help_text='Database server name', max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='config',
            name='db_username',
            field=models.CharField(help_text='Database username', max_length=64, null=True),
        ),
    ]