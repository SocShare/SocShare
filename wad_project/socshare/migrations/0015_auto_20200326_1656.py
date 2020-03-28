# Generated by Django 3.0.3 on 2020-03-26 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socshare', '0014_auto_20200326_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='banner',
            field=models.ImageField(default='event_banner/default.png', upload_to='event_banner'),
        ),
        migrations.AlterField(
            model_name='society',
            name='banner',
            field=models.ImageField(default='profile_banner/default.png', upload_to='profile_banner'),
        ),
        migrations.AlterField(
            model_name='society',
            name='profile',
            field=models.ImageField(default='profile/default.jpg', upload_to='profile'),
        ),
    ]