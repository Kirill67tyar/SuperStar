# Generated by Django 4.2.10 on 2024-10-15 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_employee_image'),
        ('trainings', '0004_alter_developmentplanrequest_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Время оценки')),
                ('score', models.PositiveSmallIntegerField(verbose_name='Рейтинг')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='employees.employee', verbose_name='Сотрудник')),
            ],
            options={
                'verbose_name': 'Рейтинг',
                'verbose_name_plural': 'Рейтинги',
                'ordering': ('date', 'employee'),
            },
        ),
        migrations.AddConstraint(
            model_name='rating',
            constraint=models.UniqueConstraint(fields=('employee', 'date'), name='unique_employee_date_rating'),
        ),
    ]