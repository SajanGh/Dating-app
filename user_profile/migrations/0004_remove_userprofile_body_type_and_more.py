# Generated by Django 4.0.6 on 2022-07-31 08:16

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_userprofile_body_type_userprofile_education_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='body_type',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='education',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='eye_color',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='hair_colour',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='hair_length',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='looking_for',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='relationship_status',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='religion',
        ),
        migrations.CreateModel(
            name='UserDescription',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('eye_color', models.CharField(choices=[('BLACK', 'Black'), ('BROWN', 'Brown'), ('BLUE', 'Blue'), ('GREEN', 'Green'), ('HAZEL', 'Hazel'), ('OTHER', 'Other')], default='BLACK', max_length=10)),
                ('hair_length', models.CharField(choices=[('LONG', 'Long'), ('SHOULDER LENGTH', 'Shoulder Length'), ('AVERAGE', 'Average'), ('SHORT', 'Short'), ('SHAVED', 'Shaved')], default='LONG', max_length=100)),
                ('hair_colour', models.CharField(choices=[('BLACK', 'Black'), ('BLONDE', 'Blonde'), ('BROWN', 'Brown'), ('RED', 'Red'), ('GREY', 'Grey'), ('BALD', 'Bald'), ('BLUE', 'Blue'), ('PINK', 'Pink'), ('GREEN', 'Green'), ('PURPLE', 'Purple'), ('OTHER', 'Other')], default='BLACK', max_length=10)),
                ('body_type', models.CharField(choices=[('THIN', 'Thin'), ('AVERAGE', 'Average'), ('FIT', 'Fit'), ('MUSCULAR', 'Muscular'), ('A LITTLE EXTRA', 'A Little Extra'), ('CURVY', 'Curvy')], default='AVERAGE', max_length=15)),
                ('religion', models.CharField(choices=[('HINDU', 'Hindu'), ('CHRISTIAN', 'Christian'), ('MUSLIM', 'Muslim'), ('BUDDHIST', 'Buddhist'), ('OTHER', 'Other')], default='HINDU', max_length=100)),
                ('relationship_status', models.CharField(choices=[('SINGLE', 'Single'), ('WIDOWED', 'Widowed'), ('SEPARATED', 'Separated')], default='SINGLE', max_length=100)),
                ('education', models.CharField(choices=[('HIGH SCHOOL', 'High School'), ('COLLEGE', 'College'), ('BACHELORS DEGREE', 'Bachelors Degree'), ('MASTERS', 'Masters'), ('PHD / POST DOCTORAL', 'PhD / Post Doctoral')], default='HIGH SCHOOL', max_length=100)),
                ('looking_for', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('BOTH', 'Both')], default='BOTH', max_length=6)),
                ('is_completed', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='description', to='user_profile.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
