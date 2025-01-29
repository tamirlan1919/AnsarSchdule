# Generated by Django 5.1 on 2025-01-27 11:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='extralesson',
            name='is_online',
            field=models.BooleanField(default=False, verbose_name='Онлайн-формат'),
        ),
        migrations.AddField(
            model_name='extralesson',
            name='room',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.room', verbose_name='Квартира'),
        ),
        migrations.AlterField(
            model_name='extralesson',
            name='groupe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.group', verbose_name='Основная группа'),
        ),
    ]
