# Generated by Django 5.0.6 on 2024-07-13 13:07

import utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0024_alter_brand_image_name_alter_product_image_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='image_name',
            field=models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر برند '),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_name',
            field=models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر کالا'),
        ),
        migrations.AlterField(
            model_name='productgallery',
            name='image_name',
            field=models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر کالا'),
        ),
        migrations.AlterField(
            model_name='productgroup',
            name='image_name',
            field=models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر گروه کالا'),
        ),
    ]
