# Generated by Django 5.0.6 on 2024-06-17 20:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='register_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ پرداخت'),
        ),
    ]