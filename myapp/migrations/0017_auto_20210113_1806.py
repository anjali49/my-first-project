# Generated by Django 3.0 on 2021-01-13 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_auto_20210113_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='status',
            field=models.CharField(default='pending', max_length=100),
        ),
        migrations.AlterField(
            model_name='cart',
            name='net_amount',
            field=models.CharField(default='0', max_length=100),
        ),
    ]
