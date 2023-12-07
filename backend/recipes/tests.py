from django.urls import reverse
from rest_framework import status
from test_plus.test import APITestCase
from .factories import UserFactory, IngredientFactory, RecipeIngredientFactory, RecipeStepFactory, RecipeFactory
from .models import RecipeIngredient, RecipeStep, Ingredient, Recipe

class RecipeTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.recipe = RecipeFactory(user=self.user)
        self.ingredient = IngredientFactory()
        self.recipe_ingredient = RecipeIngredientFactory(recipe=self.recipe, ingredient=self.ingredient)
        self.recipe_step = RecipeStepFactory(recipe=self.recipe)

    def test_list_recipe(self):
        url = reverse('recipe-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_recipe(self):
        response = self.client.get(reverse('recipe-detail', kwargs={'pk': self.recipe.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_recipe(self):
        data = {
            "title": "Test Recipe",
            "prep_time": 30,
            "diff_lvl": "Easy",
            "ingredients": [
                {
                    "ingredient": {
                        "ingredient_name": "Test Ingredient"
                    },
                    "amount": 1,
                    "measure": "cup"
                }
            ],
            "steps": [
                {
                    "step_number": 1,
                    "description": "Test Step"
                }
            ]
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('recipe-list'), data, format='json')
        self.assertContains(response, 'id', status_code=status.HTTP_201_CREATED)
        
        # Check if recipe is created
        self.assertEqual(Recipe.objects.count(), 2)
        self.assertEqual(Recipe.objects.all()[1].title, "Test Recipe")
    
        # Check if ingredient is created
        self.assertEqual(Ingredient.objects.count(), 2)
        self.assertEqual(Ingredient.objects.all()[1].ingredient_name, "test ingredient")
    
        # Check if recipe ingredient is created
        self.assertEqual(RecipeIngredient.objects.count(), 2)
        self.assertEqual(RecipeIngredient.objects.all()[1].amount, 1)
        self.assertEqual(RecipeIngredient.objects.all()[1].measure, "cup")
    
        # Check if step is created
        self.assertEqual(RecipeStep.objects.count(), 2)
        self.assertEqual(RecipeStep.objects.all()[1].step_number, 1)
        self.assertEqual(RecipeStep.objects.all()[1].description, "Test Step")
    
    def test_update_recipe(self):
        data = {
            "title": "Test Recipe 2",
            "prep_time": 15,
            "diff_lvl": "Intermediate",
            "ingredients": [
                {
                    "id": self.recipe_ingredient.id,
                    "ingredient": {
                        "ingredient_name": "Test Ingredient 2"
                    },
                    "amount": 100,
                    "measure": "g"
                }
            ],
            "steps": [
                {
                    "id": self.recipe_step.id,
                    "step_number": 1,
                    "description": "Test Step"
                },
                {
                    "step_number": 2,
                    "description": "Test Step 2"
                }
            ]
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('recipe-detail', kwargs={'pk': self.recipe.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], data['title'])