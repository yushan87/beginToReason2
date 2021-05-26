# Generated by Django 3.1.8 on 2021-04-13 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('accounts', '0002_auto_20210412_2037'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinformation',
            name='completed_sets',
            field=models.ManyToManyField(blank=True, related_name='sets_completed', to='core.MainSet'),
        ),
    ]
