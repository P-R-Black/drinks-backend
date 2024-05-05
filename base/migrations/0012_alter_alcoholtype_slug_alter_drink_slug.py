# Generated by Django 4.2.5 on 2024-04-29 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_drinkrecipe_slug_alter_drinkrecipe_serving_glass'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alcoholtype',
            name='slug',
            field=models.SlugField(blank=True, db_index=False, max_length=250),
        ),
        migrations.AlterField(
            model_name='drink',
            name='slug',
            field=models.SlugField(blank=True, db_index=False, max_length=250),
        ),
    ]