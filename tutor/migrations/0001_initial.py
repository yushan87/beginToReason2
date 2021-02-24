# Generated by Django 3.1.7 on 2021-02-23 01:34

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('lesson_index', models.IntegerField(default=0)),
                ('lesson_key', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='core.lesson')),
                ('lesson_set_key', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='core.lessonset')),
                ('main_set_key', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.mainset')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
