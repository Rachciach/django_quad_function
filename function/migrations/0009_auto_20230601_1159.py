# Generated by Django 3.2.10 on 2023-06-01 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('function', '0008_auto_20230601_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quadfunction',
            name='end_x',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='quadfunction',
            name='range_plot',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='quadfunction',
            name='start_x',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]
