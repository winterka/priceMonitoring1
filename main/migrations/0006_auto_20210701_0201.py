# Generated by Django 3.2.3 on 2021-06-30 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210701_0142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complete',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='complete',
            name='price',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
