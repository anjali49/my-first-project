# Generated by Django 3.0 on 2021-01-06 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_auto_20210101_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='net_amount',
            field=models.CharField(default='0', max_length=100),
        ),
    ]