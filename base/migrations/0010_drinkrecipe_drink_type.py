# Generated by Django 4.2.5 on 2024-04-28 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_remove_drinkrecipe_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='drinkrecipe',
            name='drink_type',
            field=models.CharField(choices=[('cocktail', 'Cocktail'), ('shot', 'Shot')], default='cocktail', max_length=10),
        ),
    ]
