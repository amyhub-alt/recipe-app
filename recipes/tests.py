from django.test import TestCase
from django.urls import reverse
from .models import Recipe

class RecipeModelTest(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(
            name="Test Grilled Cheese",
            cooking_time=10,
            ingredients="Bread, Cheese, Butter",
            description="Simple and delicious",
            difficulty="Easy"
        )

    def test_recipe_creation(self):
        self.assertEqual(self.recipe.name, "Test Grilled Cheese")
        self.assertEqual(self.recipe.difficulty, "Easy")
        self.assertTrue(isinstance(self.recipe, Recipe))

class RecipeViewsTest(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(
            name="Test Grilled Cheese",
            cooking_time=10,
            ingredients="Bread, Cheese, Butter",
            description="Simple and delicious",
            difficulty="Easy"
        )

    def test_homepage_loads(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_list_loads(self):
        response = self.client.get(reverse('recipes:list'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_loads(self):
        response = self.client.get(reverse('recipes:detail', kwargs={'pk': self.recipe.pk}))
        self.assertEqual(response.status_code, 200)
