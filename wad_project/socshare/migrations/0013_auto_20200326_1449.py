# Generated by Django 3.0.3 on 2020-03-26 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socshare', '0012_event_description_short'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='banner',
            field=models.ImageField(default='default.png', upload_to='event_banner'),
        ),
        migrations.AlterField(
            model_name='society',
            name='banner',
            field=models.ImageField(default='test.png', upload_to='profile_banner'),
        ),
    ]