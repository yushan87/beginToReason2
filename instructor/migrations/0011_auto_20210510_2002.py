# Generated by Django 3.1.8 on 2021-05-11 00:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20210509_1552'),
        ('instructor', '0010_auto_20210509_0956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignmentprogress',
            name='completed_lesson_index',
        ),
        migrations.RemoveField(
            model_name='assignmentprogress',
            name='current_lesson_index',
        ),
        migrations.AddField(
            model_name='assignmentprogress',
            name='alternate_level',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='assignmentprogress',
            name='current_lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.lesson'),
        ),
        migrations.AlterField(
            model_name='assignmentprogress',
            name='current_lesson_set',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.lessonset'),
        ),
    ]
