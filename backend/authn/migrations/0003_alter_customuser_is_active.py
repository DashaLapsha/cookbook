# Generated by Django 4.2.5 on 2023-10-17 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authn', '0002_alter_customuser_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
    ]
