# Generated by Django 3.1.8 on 2021-05-11 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educator', '0011_auto_20210510_2002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignmentprogress',
            name='current_lesson',
        ),
        migrations.RemoveField(
            model_name='assignmentprogress',
            name='current_lesson_set',
        ),
        migrations.AddField(
            model_name='assignmentprogress',
            name='current_lesson_index',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='assignmentprogress',
            name='current_set_index',
            field=models.IntegerField(default=0),
        ),
    ]
