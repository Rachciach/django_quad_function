# Generated by Django 3.2.10 on 2023-06-09 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('function', '0009_auto_20230601_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quadfunction',
            name='end_x',
            field=models.SmallIntegerField(blank=True, default=5, null=True),
        ),
        migrations.AlterField(
            model_name='quadfunction',
            name='start_x',
            field=models.SmallIntegerField(blank=True, default=-5, null=True),
        ),
    ]
