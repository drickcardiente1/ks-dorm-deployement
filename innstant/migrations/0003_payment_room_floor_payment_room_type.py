# Generated by Django 4.1 on 2023-04-07 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('innstant', '0002_alter_payment_tenant'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='room_floor',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='room_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
