# Generated by Django 3.2.14 on 2022-08-03 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_availability', '0011_auto_20220803_0820'),
    ]

    operations = [
        migrations.RenameField(
            model_name='config',
            old_name='data_Store_query',
            new_name='data_store_query',
        ),
    ]
