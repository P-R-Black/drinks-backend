# Generated by Django 4.2.5 on 2023-09-16 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_drinkrecipe_created_drinkrecipe_updated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drinkrecipe',
            name='base_alcohol',
            field=models.ManyToManyField(related_name='base_alcohol', to='base.alcoholtype'),
        ),
        migrations.AlterField(
            model_name='drinkrecipe',
            name='garnish',
            field=models.ManyToManyField(related_name='garnish', to='base.garnish'),
        ),
        migrations.AlterField(
            model_name='drinkrecipe',
            name='ingredient_name',
            field=models.ManyToManyField(blank=True, to='base.ingredientname'),
        ),
    ]