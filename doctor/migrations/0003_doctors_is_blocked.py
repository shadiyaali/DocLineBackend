# Generated by Django 4.2.1 on 2023-06-19 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_slots_appointment'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctors',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
    ]
