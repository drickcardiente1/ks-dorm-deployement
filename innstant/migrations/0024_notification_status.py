# Generated by Django 4.1 on 2023-04-29 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('innstant', '0023_extendstay_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='status',
            field=models.CharField(choices=[('Read', 'Read'), ('Pending', 'Pending')], default='Pending', max_length=10),
        ),
    ]