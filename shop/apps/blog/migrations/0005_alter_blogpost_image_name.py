# Generated by Django 5.0.6 on 2024-10-03 09:18

import utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_blogpost_image_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='image_name',
            field=models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر کالا'),
        ),
    ]
