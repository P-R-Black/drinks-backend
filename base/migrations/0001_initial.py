# Generated by Django 4.2.14 on 2024-10-05 19:25

from decimal import Decimal
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
                ('name', models.CharField(blank=True, max_length=250, unique=True)),
                ('slug', models.SlugField(db_index=False, max_length=250, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Drink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('slug', models.SlugField(db_index=False, max_length=250, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='FlavorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServingGlass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'Serving Glass',
                'verbose_name_plural': 'Serving Glasses',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('value', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=5, null=True)),
                ('measurement', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'ordering': ['name'],
                'unique_together': {('name', 'measurement', 'value')},
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
                'unique_together': {('name', 'value')},
            },
        ),
        migrations.CreateModel(
            name='DrinkRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mixing_direction', models.TextField(null=True)),
                ('drink_type', models.CharField(choices=[('cocktail', 'Cocktail'), ('shot', 'Shot')], default='cocktail', max_length=10)),
                ('must_know_drink', models.BooleanField(default=False)),
                ('top_hundred_drink', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('base_alcohol', models.ManyToManyField(related_name='recipes', to='base.alcoholtype')),
                ('drink', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='base.drink')),
                ('flavor_profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='base.flavorprofile')),
                ('garnish', models.ManyToManyField(related_name='recipes', to='base.garnish')),
                ('ingredients', models.ManyToManyField(blank=True, related_name='recipes', to='base.ingredient')),
                ('serving_glass', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='recipes', to='base.servingglass')),
            ],
            options={
                'verbose_name': 'Drink Recipe',
                'verbose_name_plural': 'Drink Recipes',
            },
        ),
    ]
