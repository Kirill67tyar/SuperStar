# Generated by Django 4.2.10 on 2024-10-10 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Фамилия Имя')),
                ('bus_factor', models.BooleanField(default=False, verbose_name='Автобусный фактор')),
                ('created', models.DateField(verbose_name='Добавлено')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Junior', 'Junior'), ('Middle', 'Middle'), ('Senior', 'Senior')], max_length=20)),
            ],
            options={
                'verbose_name': 'Домен',
                'verbose_name_plural': 'Домены',
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Должность',
                'verbose_name_plural': 'Должности',
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Команда',
                'verbose_name_plural': 'Команды',
            },
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='employees.employee', verbose_name='Сотрудник')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.grade', verbose_name='Грейд')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.position', verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'Карьерная цель',
                'verbose_name_plural': 'Карьерные цели',
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='grade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.grade', verbose_name='Грейд'),
        ),
        migrations.AddField(
            model_name='employee',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.position', verbose_name='Дожность'),
        ),
        migrations.AddField(
            model_name='employee',
            name='team',
            field=models.ManyToManyField(related_name='employees', to='employees.team', verbose_name='Команды'),
        ),
    ]
