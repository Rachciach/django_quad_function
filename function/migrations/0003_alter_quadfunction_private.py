# Generated by Django 3.2.10 on 2023-04-17 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('function', '0002_quadfunction_private'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quadfunction',
            name='private',
            field=models.BooleanField(default=True),
        ),
    ]
