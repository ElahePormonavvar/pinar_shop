# Generated by Django 5.0.6 on 2024-06-02 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='disscount',
            new_name='discount',
        ),
    ]
