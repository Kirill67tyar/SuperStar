# Generated by Django 4.2.10 on 2024-10-05 10:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0005_rename_name_level_level_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainigrequest',
            name='desired_score',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Оценка не может быть меньше 1'), django.core.validators.MaxValueValidator(5, message='Оценка не может быть больше 5')], verbose_name='Желаемая оценка сотрудника'),
        ),
    ]