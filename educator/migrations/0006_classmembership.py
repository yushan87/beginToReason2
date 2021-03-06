# Generated by Django 3.1.8 on 2021-04-20 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210420_0527'),
        ('educator', '0005_auto_20210413_1747'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_educator', models.BooleanField(default=False)),
                ('class_taking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='educator.class')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.userinformation')),
            ],
        ),
    ]
