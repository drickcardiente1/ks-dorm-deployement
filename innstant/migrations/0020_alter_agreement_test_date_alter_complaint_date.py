# Generated by Django 4.1 on 2023-04-21 19:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('innstant', '0019_alter_complaint_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agreement',
            name='test_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]