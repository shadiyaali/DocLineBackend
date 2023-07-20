# Generated by Django 4.2.1 on 2023-07-20 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0012_appointment_appointment_payment_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('completed', 'Completed'), ('rejected', 'Rejected')], default='pending', max_length=20),
        ),
    ]
