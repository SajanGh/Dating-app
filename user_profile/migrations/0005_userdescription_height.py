# Generated by Django 4.0.6 on 2022-07-31 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0004_remove_userprofile_body_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdescription',
            name='height',
            field=models.CharField(choices=[('BELOW 4', 'Below 4'), ('4 to 5', '4 to 5'), ('5 to 6', '5 to 6'), ('ABOVE 6', 'Above 6')], default='4 to 5', max_length=10),
        ),
    ]
