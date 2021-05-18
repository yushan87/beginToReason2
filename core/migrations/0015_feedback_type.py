# Generated by Django 3.1.8 on 2021-05-18 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_lessonalternate_replace'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='type',
            field=models.IntegerField(choices=[(0, 'Default'), (1, 'Simplify'), (2, 'Self Reference'), (3, 'Used Concrete Value as Answer'), (4, 'Missing # Symbol'), (5, 'Algebra'), (6, 'Variable')], default=-1),
            preserve_default=False,
        ),
    ]
