# Generated by Django 4.1 on 2023-04-19 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('innstant', '0005_agreement_rules'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agreement',
            name='rules',
        ),
        migrations.AddField(
            model_name='roomtype',
            name='room_legend',
            field=models.CharField(default='Room Type Name', max_length=20),
        ),
    ]
