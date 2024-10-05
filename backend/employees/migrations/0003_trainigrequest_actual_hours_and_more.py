# Generated by Django 4.2.10 on 2024-10-05 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_rename_grade_grade_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainigrequest',
            name='actual_hours',
            field=models.PositiveSmallIntegerField(default=1000, verbose_name='Часов по факту'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trainigrequest',
            name='planned_hours',
            field=models.PositiveSmallIntegerField(default=1000, verbose_name='Запланированные часы'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='trainigrequest',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата окончания обучения'),
        ),
    ]
