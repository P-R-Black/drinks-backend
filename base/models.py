from django.db import models
from django.urls import reverse
from decimal import Decimal


# Create your models here.
class IngredientName(models.Model):
    ingredient = models.CharField(max_length=250)
    drink_recipe = models.ForeignKey("DrinkRecipe",
                                     related_name="ingredient_list",
                                     blank=True,
                                     on_delete=models.CASCADE,
                                     unique=False,
                                     null=True)
    value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
    measurement = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ['ingredient', 'measurement', 'value']
        ordering = ['ingredient']

    def __str__(self):
        return '%s %s %s' % (self.value, self.measurement, self.ingredient)


class Garnish(models.Model):
    name = models.CharField(max_length=250)
    value = models.IntegerField(blank=True, default=None, null=True)

    class Meta:
        verbose_name = "Garnish"
        verbose_name_plural = "Garnishes"
        unique_together = ['name', 'value']
        ordering = ['name']

    def __str__(self):
        return '%d %s' % (self.value, self.name)


class AlcoholType(models.Model):
    spirit_type = models.CharField(max_length=250, blank=True, unique=True)

    def __str__(self):
        return self.spirit_type


class Drink(models.Model):
    drink_name = models.CharField(max_length=250, blank=False, unique=True)

    def __str__(self):
        return self.drink_name


class ServingGlass(models.Model):
    name = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name = "Serving Glass"
        verbose_name_plural = "Serving Glasses"

    def __str__(self):
        return self.name


class FlavorProfile(models.Model):
    profile = models.CharField(max_length=50, null=True)

    class Meta:
        verbose_name = "Flavor Profile"
        verbose_name_plural = "Flavor Profiles"

    def __str__(self):
        return self.profile


class DrinkRecipe(models.Model):

    class DrinkRecipeObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset()

    drink = models.ForeignKey(Drink, related_name='drink', on_delete=models.CASCADE)
    flavor_profile = models.ForeignKey(FlavorProfile,
                                       related_name='flavor_profile',
                                       on_delete=models.CASCADE,
                                       null=True,
                                       )
    base_alcohol = models.ManyToManyField(AlcoholType, related_name="base_alcohol")
    ingredient_name = models.ManyToManyField(IngredientName, blank=True)
    garnish = models.ManyToManyField(Garnish, related_name="garnish")
    serving_glass = models.ForeignKey(ServingGlass, null=True, related_name="serving_glass", on_delete=models.CASCADE)
    mixing_direction = models.TextField(max_length=None, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    drinkobjects = DrinkRecipeObjects()

    class Meta:
        verbose_name = "Drink Recipe"
        verbose_name_plural = "Drink Recipes"

    def __str__(self):
        base_alcohol = ''.join(str(b) for b in self.base_alcohol.all())
        ingredient_name = ', '.join(str(v) for v in self.ingredient_name.all())
        garnish = ''.join(str(g) for g in self.garnish.all())
        return '%s %s %s %s %s' % (self.drink.drink_name, base_alcohol, ingredient_name,
                                   garnish, self.serving_glass)
