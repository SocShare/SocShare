# Generated by Django 3.0.3 on 2020-03-31 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socshare', '0015_auto_20200326_1656'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
        migrations.AddField(
            model_name='comment',
            name='token',
            field=models.TextField(default='1'),
            preserve_default=False,
        ),
    ]
