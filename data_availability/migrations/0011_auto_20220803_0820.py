# Generated by Django 3.2.14 on 2022-08-03 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_availability', '0010_alter_feature_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feature',
            name='query',
        ),
        migrations.AddField(
            model_name='config',
            name='data_Store_query',
            field=models.CharField(help_text='Feature query', max_length=256, null=True),
        ),
    ]
