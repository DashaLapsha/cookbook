# Generated by Django 4.2.5 on 2023-11-01 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='title_img',
            field=models.ImageField(upload_to='recipe_images/'),
        ),
    ]
