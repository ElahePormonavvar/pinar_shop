# Generated by Django 5.0.6 on 2024-07-01 11:41

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment_scoring_favorites', '0002_alter_comment_approviding_user'),
        ('products', '0022_alter_brand_image_name_alter_product_image_name_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Scoring',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registerdate', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')),
                ('score', models.PositiveBigIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='امتیاز')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scoring_product', to='products.product', verbose_name='کالا')),
                ('scoring_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scoring_user1', to=settings.AUTH_USER_MODEL, verbose_name='کاربرامتیازدهنده')),
            ],
            options={
                'verbose_name': 'امتیاز',
                'verbose_name_plural': 'امتیازات',
            },
        ),
    ]
