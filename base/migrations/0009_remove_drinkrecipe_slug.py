# Generated by Django 4.2.5 on 2024-04-28 00:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_drinkrecipe_slug_alter_drinkrecipe_ingredient_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drinkrecipe',
            name='slug',
        ),
    ]
