# Generated by Django 5.0.6 on 2024-07-15 14:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_alter_order_register_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='register_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='تاریخ درج سفارش'),
        ),
    ]