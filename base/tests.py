from django.test import TestCase
from base.models import (IngredientName, Garnish, AlcoholType, Drink, ServingGlass, FlavorProfile, DrinkRecipe)


# Create your tests here.
class Test_Create_IngredientName(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_ingredients = IngredientName.objects.create(ingredient="TestGin", value=1, measurement="Ounce")
        test_garnish = Garnish.objects.create(name="Orange Slice", value=1)
        test_alcohol_type = AlcoholType.objects.create(spirit_type="Gin")
        test_drink = Drink.objects.create(drink_name="Gin & Tonic")
        test_service_glass = ServingGlass.objects.create(name="Highball")
        test_flavor_profile = FlavorProfile.objects.create(profile="Sweet")

        test_drink_recipe = DrinkRecipe.objects.create(drink=test_drink)
        test_drink_recipe.flavor_profile = test_flavor_profile
        test_drink_recipe.base_alcohol.set([test_alcohol_type])
        test_drink_recipe.ingredient_name.set([test_ingredients])
        test_drink_recipe.garnish.set([test_garnish])
        test_drink_recipe.serving_glass = test_service_glass
        test_drink_recipe.mixing_direction = "Add ice, mix well."


    def test_drink_recipe(self):
        recipe = DrinkRecipe.objects.get(id=1)
        test_ingredients = IngredientName.objects.create(ingredient="Rum", value=1, measurement="Ounce")
        test_garnish = Garnish.objects.create(name="Lime Wheels", value=2)
        test_alcohol_type = AlcoholType.objects.create(spirit_type="Rum")
        test_drink = Drink.objects.create(drink_name="Rum & Coke")
        test_service_glass = ServingGlass.objects.create(name="Highball")
        test_flavor_profile = FlavorProfile.objects.create(profile="Sweet")

        test_name = f"{test_drink}"
        test_ingred = f"{test_ingredients}"
        test_garn = f"{test_garnish}"
        test_alc_type = f"{test_alcohol_type}"
        test_serv_glass = f"{test_service_glass}"
        test_flavor = f"{test_flavor_profile}"

        self.assertEqual(first=test_name, second="Rum & Coke")
        self.assertEqual(first=test_ingred, second="1 Ounce Rum")
        self.assertEqual(first=test_garn, second="2 Lime Wheels")
        self.assertEqual(first=test_alc_type, second="Rum")
        self.assertEqual(first=test_serv_glass, second="Highball")
        self.assertEqual(first=test_flavor, second="Sweet")

    def test_ingredient_content(self):
        ingred = IngredientName.objects.get(id=1)

        ingredient_name = f'{ingred.ingredient}'
        ingredient_value = f'{ingred.value}'
        ingredient_measurement = f'{ingred.measurement}'

        self.assertEqual(ingredient_name, 'TestGin')
        self.assertEqual(ingredient_value, "1.00")
        self.assertEqual(ingredient_measurement, 'Ounce')

        self.assertEqual(str(ingred), "1.00 Ounce TestGin")

    def test_garnish_content(self):
        garn = Garnish.objects.get(id=1)
        garnish_name = f'{garn.name}'
        garnish_value = f'{garn.value}'

        self.assertEqual(garnish_name, 'Orange Slice')
        self.assertEqual(garnish_value, "1")
        self.assertEqual(str(garn), "1 Orange Slice")

    def test_alcohol_type_content(self):
        at = AlcoholType.objects.get(id=1)
        alcohol_type = f'{at.spirit_type}'

        self.assertEqual(alcohol_type, 'Gin')
        self.assertEqual(str(at), "Gin")

    def test_drink_content(self):
        dr = Drink.objects.get(id=1)
        drink = f'{dr.drink_name}'

        self.assertEqual(drink, 'Gin & Tonic')
        self.assertEqual(str(dr), "Gin & Tonic")

    def test_service_glass(self):
        glass = ServingGlass.objects.get(id=1)
        serv_glass = f'{glass.name}'

        self.assertEqual(serv_glass, 'Highball')
        self.assertEqual(str(glass), "Highball")

    def test_flavor_profile(self):
        fp = FlavorProfile.objects.get(id=1)
        flavor = f'{fp.profile}'

        self.assertEqual(flavor, 'Sweet')
        self.assertEqual(str(fp), "Sweet")
