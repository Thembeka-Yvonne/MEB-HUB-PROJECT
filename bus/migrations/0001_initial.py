# Generated by Django 5.1.4 on 2025-03-11 08:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0004_alter_student_stud_card_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('bus_id', models.IntegerField(primary_key=True, serialize=False)),
                ('bus_name', models.CharField(max_length=255)),
                ('campus_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.campus')),
            ],
        ),
        migrations.CreateModel(
            name='Bus_schedule',
            fields=[
                ('schedule_id', models.IntegerField(primary_key=True, serialize=False)),
                ('departure', models.CharField(max_length=255)),
                ('destination', models.CharField(max_length=255)),
                ('departure_time', models.TimeField()),
                ('arrival_time', models.TimeField()),
                ('duration', models.IntegerField()),
                ('bus_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bus.bus')),
            ],
        ),
    ]
