# Generated by Django 4.0.6 on 2022-07-18 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(null=True, upload_to='profile_images'),
        ),
    ]