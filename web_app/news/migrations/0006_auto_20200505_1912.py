# Generated by Django 3.0.6 on 2020-05-05 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_auto_20200505_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='avatar',
            field=models.ImageField(default=None, upload_to='images/avatars'),
        ),
    ]