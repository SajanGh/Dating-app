# Generated by Django 4.0.6 on 2022-08-05 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0006_userprofile_age_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='zodiac',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]