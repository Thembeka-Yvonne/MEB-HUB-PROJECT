# Generated by Django 5.1.4 on 2025-03-03 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='student',
            name='surname',
            field=models.CharField(default='', max_length=100),
        ),
    ]
