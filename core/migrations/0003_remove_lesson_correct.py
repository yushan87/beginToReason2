# Generated by Django 3.1.8 on 2021-05-09 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_lesson_correct_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='correct',
        ),
    ]
