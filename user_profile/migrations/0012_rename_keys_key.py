# Generated by Django 4.0.6 on 2022-08-21 19:29

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_profile', '0011_keys'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Keys',
            new_name='Key',
        ),
    ]