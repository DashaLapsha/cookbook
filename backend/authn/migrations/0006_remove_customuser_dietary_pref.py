# Generated by Django 4.2.5 on 2024-05-02 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authn', '0005_customuser_profile_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='dietary_pref',
        ),
    ]
