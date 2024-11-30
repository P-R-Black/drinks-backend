from django.db import models
from decimal import Decimal
from django.utils.text import slugify


# Ingredient Model
class Ingredient(models.Model):
    name = models.CharField(max_length=250)
    value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=Decimal(0.00))
    measurement = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ['name', 'measurement', 'value']
        ordering = ['name']

    def __str__(self):
        return '%s %s %s' % (self.value, self.measurement, self.name)


# Garnish Model
class Garnish(models.Model):
    name = models.CharField(max_length=250)
    value = models.IntegerField(blank=True, default=None, null=True)
    measurement = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Garnish"
        verbose_name_plural = "Garnishes"
        unique_together = ['name', 'measurement', 'value']
        ordering = ['name']

    def __str__(self):
        return '%s %s %s' % (self.value, self.measurement, self.name)


# Alcohol Base Model
class AlcoholType(models.Model):
    name = models.CharField(max_length=250, blank=True, unique=True)
    slug = models.SlugField(max_length=250, db_index=True, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# Drink Name Model:
class Drink(models.Model):
    name = models.CharField(max_length=250, blank=False, unique=True)
    slug = models.SlugField(max_length=250, db_index=True, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# Serving Glass Model
class ServingGlass(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True)

    class Meta:
        verbose_name = "Serving Glass"
        verbose_name_plural = "Serving Glasses"
        ordering = ['name']

    def __str__(self):
        return self.name


# Flavor Profile Model
class FlavorProfile(models.Model):
    profile = models.CharField(max_length=50, null=True, unique=True)

    class Meta:
        ordering = ['profile']

    def __str__(self):
        return self.profile


# Drink Recipe Model
class DrinkRecipe(models.Model):
    DRINK_TYPE_CHOICES = (
        ('cocktail', 'Cocktail'),
        ('shot', 'Shot'),
    )

    drink = models.ForeignKey(Drink, related_name='recipes', on_delete=models.CASCADE)
    flavor_profile = models.ForeignKey(FlavorProfile, related_name='recipes', on_delete=models.CASCADE, null=True)
    base_alcohol = models.ManyToManyField(AlcoholType, related_name="recipes")
    ingredients = models.ManyToManyField(Ingredient, related_name="recipes", blank=True)
    garnish = models.ManyToManyField(Garnish, related_name="recipes")
    serving_glass = models.ForeignKey(ServingGlass, null=True, related_name="recipes", on_delete=models.PROTECT)
    mixing_direction = models.TextField(null=True)
    drink_type = models.CharField(max_length=10, choices=DRINK_TYPE_CHOICES, default='cocktail')
    must_know_drink = models.BooleanField(default=False)
    top_hundred_drink = models.BooleanField(default=False)
    # slug = models.SlugField(max_length=250, db_index=True, unique=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Drink Recipe"
        verbose_name_plural = "Drink Recipes"

    def __str__(self):
        base_alcohol_names = ', '.join(b.name for b in self.base_alcohol.all())
        ingredient_names = ', '.join(i.name for i in self.ingredients.all())
        garnish_names = ', '.join(g.name for g in self.garnish.all())
        return '%s %s %s %s %s' % (
            self.drink.name, base_alcohol_names, ingredient_names, garnish_names, self.serving_glass.name
        )

