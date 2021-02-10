# Generated by Django 3.1.2 on 2021-02-10 02:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('accounts', '0003_auto_20210206_1459'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinformation',
            name='current_main_set',
        ),
        migrations.AddField(
            model_name='userinformation',
            name='current_main_set',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.mainset'),
        ),
    ]
