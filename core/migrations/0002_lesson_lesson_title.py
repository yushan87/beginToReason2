# Generated by Django 3.0.8 on 2020-07-07 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='lesson_title',
            field=models.CharField(default='default', max_length=50),
        ),
    ]
