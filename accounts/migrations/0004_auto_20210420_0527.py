# Generated by Django 3.1.8 on 2021-04-20 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userinformation_completed_sets'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinformation',
            name='user_classes',
        ),
        migrations.RemoveField(
            model_name='userinformation',
            name='user_instructor',
        ),
    ]
