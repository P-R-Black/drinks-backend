# Generated by Django 4.2.5 on 2024-05-03 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_alter_drink_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alcoholtype',
            name='slug',
            field=models.SlugField(max_length=250, unique=True),
        ),
    ]
