# Generated by Django 4.2.5 on 2024-04-27 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alcoholtype_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='drink',
            name='slug',
            field=models.SlugField(blank=True, max_length=250),
        ),
    ]