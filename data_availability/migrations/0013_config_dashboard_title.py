# Generated by Django 3.2.14 on 2022-09-05 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_availability', '0012_rename_data_store_query_config_data_store_query'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='dashboard_title',
            field=models.CharField(help_text='Dashboard title', max_length=64, null=True),
        ),
    ]
