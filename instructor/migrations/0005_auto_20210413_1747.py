# Generated by Django 3.1.8 on 2021-04-13 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('instructor', '0004_auto_20210413_1031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='lesson_sets',
        ),
        migrations.AddField(
            model_name='class',
            name='main_sets',
            field=models.ManyToManyField(blank=True, related_name='classes', to='core.MainSet'),
        ),
    ]
