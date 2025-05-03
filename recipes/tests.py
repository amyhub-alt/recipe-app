from django.test import TestCase
from django.urls import reverse
from .models import Recipe
from django.contrib.auth.models import User
from .forms import RecipeSearchForm


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
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')  # Ensure user is logged in

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

    def test_recipe_list_redirects_if_not_logged_in(self):
        self.client.logout()  # explicitly log out first
        response = self.client.get(reverse('recipes:list'))
        self.assertRedirects(response, '/login/?next=/recipes/list/')

    def test_recipe_list_loads_for_logged_in_user(self):
        response = self.client.get(reverse('recipes:list'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_redirects_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('recipes:detail', kwargs={'pk': self.recipe.pk}))
        self.assertRedirects(response, f'/login/?next=/recipes/list/{self.recipe.pk}/')

    def test_recipe_detail_loads_for_logged_in_user(self):
        response = self.client.get(reverse('recipes:detail', kwargs={'pk': self.recipe.pk}))
        self.assertEqual(response.status_code, 200)


class RecipeFormTest(TestCase):
    def test_form_fields_exist(self):
        form = RecipeSearchForm()
        self.assertIn('title', form.fields)
        self.assertIn('ingredient', form.fields)
        self.assertIn('chart_type', form.fields)

    def test_form_valid_data(self):
        form_data = {
            'title': 'Cheese',
            'ingredient': 'Bread',
            'chart_type': 'bar'
        }
        form = RecipeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_chart_type(self):
        form_data = {
            'title': 'Cheese',
            'ingredient': 'Bread',
            'chart_type': 'invalid_chart_type'
        }
        form = RecipeSearchForm(data=form_data)
        self.assertFalse(form.is_valid())