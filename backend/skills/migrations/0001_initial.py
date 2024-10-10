# Generated by Django 4.2.10 on 2024-10-10 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Competence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название')),
                ('type', models.CharField(choices=[('Soft skills', 'Soft skills'), ('Hard skills', 'Hard skills')], max_length=11, verbose_name='Тип скилла')),
            ],
            options={
                'verbose_name': 'Компетенция',
                'verbose_name_plural': 'Компетенции',
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название')),
                ('competence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='skills.competence', verbose_name='Компетенция')),
            ],
            options={
                'verbose_name': 'Скилл',
                'verbose_name_plural': 'Скиллы',
                'ordering': ('pk',),
            },
        ),
    ]