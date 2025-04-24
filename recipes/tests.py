from django.test import TestCase
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
