# Generated by Django 3.1.8 on 2021-05-11 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20210509_1552'),
        ('accounts', '0006_auto_20210509_0956'),
        ('educator', '0012_auto_20210510_2108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignmentprogress',
            name='alternate_level',
        ),
        migrations.CreateModel(
            name='AlternateProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_lesson_index', models.IntegerField(default=0)),
                ('alternate_level', models.IntegerField(default=0)),
                ('assignment_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='educator.assignment')),
                ('lesson_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.lessonset')),
                ('user_info_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.userinformation')),
            ],
        ),
    ]
