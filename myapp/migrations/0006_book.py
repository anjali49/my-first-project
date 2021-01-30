# Generated by Django 3.0 on 2020-12-21 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20201219_1832'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=100)),
                ('book_price', models.CharField(max_length=100)),
                ('book_image', models.ImageField(upload_to='images/')),
                ('book_desc', models.TextField()),
                ('book_subject', models.CharField(choices=[('C', 'C'), ('C++', 'C++'), ('Java', 'Java'), ('Python', 'Python'), ('PHP', 'PHP')], max_length=100)),
            ],
        ),
    ]