# Generated by Django 3.1.8 on 2021-05-09 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_analysis', '0005_auto_20210509_1148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datalog',
            name='past_answers',
        ),
    ]