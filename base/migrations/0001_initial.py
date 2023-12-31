# Generated by Django 4.2.5 on 2023-09-16 06:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlcoholType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spirit_type', models.CharField(blank=True, max_length=250, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Drink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drink_name', models.CharField(max_length=250, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DrinkRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mixing_direction', models.TextField(null=True)),
                ('base_alcohol', models.ManyToManyField(null=True, related_name='base_alcohol', to='base.alcoholtype')),
                ('drink', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drink', to='base.drink')),
            ],
            options={
                'verbose_name': 'Drink Recipe',
                'verbose_name_plural': 'Drink Recipes',
            },
        ),
        migrations.CreateModel(
            name='FlavorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.CharField(max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Flavor Profile',
                'verbose_name_plural': 'Flavor Profiles',
            },
        ),
        migrations.CreateModel(
            name='ServingGlass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Serving Glass',
                'verbose_name_plural': 'Serving Glasses',
            },
        ),
        migrations.CreateModel(
            name='IngredientName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient', models.CharField(max_length=250)),
                ('value', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=5, null=True)),
                ('measurement', models.CharField(blank=True, max_length=100, null=True)),
                ('drink_recipe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_list', to='base.drinkrecipe')),
            ],
            options={
                'ordering': ['value'],
                'unique_together': {('ingredient', 'measurement', 'value')},
            },
        ),
        migrations.CreateModel(
            name='Garnish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('value', models.IntegerField(blank=True, default=None, null=True)),
            ],
            options={
                'verbose_name': 'Garnish',
                'verbose_name_plural': 'Garnishes',
                'ordering': ['value'],
                'unique_together': {('name', 'value')},
            },
        ),
        migrations.AddField(
            model_name='drinkrecipe',
            name='flavor_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flavor_profile', to='base.flavorprofile'),
        ),
        migrations.AddField(
            model_name='drinkrecipe',
            name='garnish',
            field=models.ManyToManyField(null=True, related_name='garnish', to='base.garnish'),
        ),
        migrations.AddField(
            model_name='drinkrecipe',
            name='ingredient_name',
            field=models.ManyToManyField(blank=True, null=True, to='base.ingredientname'),
        ),
        migrations.AddField(
            model_name='drinkrecipe',
            name='serving_glass',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='serving_glass', to='base.servingglass'),
        ),
    ]
