# Generated by Django 4.1 on 2023-04-29 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('innstant', '0024_notification_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='status',
        ),
        migrations.AddField(
            model_name='notification',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
