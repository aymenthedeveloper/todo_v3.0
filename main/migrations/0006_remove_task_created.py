# Generated by Django 4.2.7 on 2023-12-06 00:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_date_options_task_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='created',
        ),
    ]
