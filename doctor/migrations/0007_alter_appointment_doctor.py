# Generated by Django 4.2.1 on 2023-07-11 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0006_appointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(limit_choices_to={'user__is_staff': True}, on_delete=django.db.models.deletion.CASCADE, to='doctor.doctors'),
        ),
    ]
