# Generated by Django 4.2.10 on 2024-10-04 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grade',
            old_name='grade',
            new_name='name',
        ),
    ]