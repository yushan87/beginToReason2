# Generated by Django 3.1.8 on 2021-05-09 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('educator', '0010_auto_20210509_0956'),
        ('data_analysis', '0003_auto_20210413_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='datalog',
            name='assignment_key',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='educator.assignment'),
        ),
    ]