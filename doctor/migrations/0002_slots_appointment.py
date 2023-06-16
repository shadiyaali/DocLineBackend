# Generated by Django 4.2.1 on 2023-06-15 04:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doctor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('status', models.BooleanField(default=True)),
                ('slot_duration', models.IntegerField()),
                ('is_booked', models.BooleanField(default=False)),
                ('doctor', models.ForeignKey(limit_choices_to={'is_active': True, 'is_staff': True, 'is_superadmin': False}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('complete', 'Complete')], default='pending', max_length=20)),
                ('conulting_fee', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date', models.DateField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('doctor', models.ForeignKey(limit_choices_to={'is_active': True, 'is_staff': True, 'is_superadmin': False}, on_delete=django.db.models.deletion.CASCADE, to='doctor.doctors')),
                ('patient', models.ForeignKey(limit_choices_to={'is_active': True, 'is_staff': False, 'is_superadmin': False}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.slots')),
            ],
        ),
    ]
