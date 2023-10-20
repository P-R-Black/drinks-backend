# Generated by Django 4.2.5 on 2023-09-16 06:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='drinkrecipe',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='drinkrecipe',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='alcoholtype',
            name='spirit_type',
            field=models.CharField(blank=True, default=django.utils.timezone.now, max_length=250, unique=True),
            preserve_default=False,
        ),
    ]