# Generated by Django 5.0.6 on 2024-06-30 14:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment_scoring_favorites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='approviding_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_user2', to=settings.AUTH_USER_MODEL, verbose_name='کاربر تایید کننده نظر'),
        ),
    ]
