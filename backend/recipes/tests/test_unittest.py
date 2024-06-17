from django.urls import reverse
from rest_framework import status
from test_plus.test import APITestCase
from ..factories import UserFactory, IngredientFactory, RecipeIngredientFactory, RecipeStepFactory, RecipeFactory, create_image
from ..models import Recipe, Ingredient, RecipeIngredient, RecipeStep
from django.core.files.uploadedfile import SimpleUploadedFile
import base64

class RecipeTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('recipe-list')

        base64_string = (
            "iVBORw0KGgoAAAANSUhEUgAAAAUA"
            "AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO"
            "9TXL0Y4OHwAAAABJRU5ErkJggg=="
        )   
        self.image_content = base64.b64decode(base64_string)

        self.title_image = SimpleUploadedFile(
            name='title_image.jpeg',
            content=self.image_content,
            content_type='image/jpeg'
        )
        
        self.step_image = SimpleUploadedFile(
            name='step_image.jpeg',
            content=self.image_content,
            content_type='image/jpeg'
        )

    def test_list_recipe(self):
        url = reverse('recipe-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_recipe(self):
        recipe = RecipeFactory(user=self.user)
        response = self.client.get(reverse('recipe-detail', kwargs={'pk': recipe.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_recipe(self):     
        data = {
            'title': 'Receive until stop what look hit expect.',
            'prep_time': 76,
            'diff_lvl': 'Easy',
            'title_img': self.title_image,
            'ingredients[0]ingredient_name': 'today',
            'ingredients[0]amount': 100,
            'ingredients[0]measure': 'grams',
            'ingredients[1]ingredient_name': 'discussion',
            'ingredients[1]amount': 2,
            'ingredients[1]measure': 'cups',
            'ingredients[2]ingredient_name': 'group',
            'ingredients[2]amount': 1,
            'ingredients[2]measure': 'teaspoon',
            'steps[0]step_number': 1,
            'steps[0]description': 'Step 1: Prepare ingredients',
            'steps[0]step_img': self.step_image,
            'steps[1]step_number': 2,
            'steps[1]description': 'Step 2: Cook for 30 minutes',
            'steps[2]step_number': 3,
            'steps[2]description': 'Step 3: Serve hot',
        }

        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify creation of recipe
        self.assertEqual(Recipe.objects.count(), 1)
        created_recipe = Recipe.objects.first()
        self.assertEqual(created_recipe.title, 'Receive until stop what look hit expect.')

        # Verify creation of ingredients
        self.assertEqual(RecipeIngredient.objects.count(), 3)  # Adjust based on actual number of ingredients created
        self.assertEqual(RecipeIngredient.objects.get(ingredient__ingredient_name='today').amount, 100)
        self.assertEqual(RecipeIngredient.objects.get(ingredient__ingredient_name='discussion').amount, 2)
        self.assertEqual(RecipeIngredient.objects.get(ingredient__ingredient_name='group').amount, 1)

        # Verify creation of steps
        self.assertEqual(RecipeStep.objects.count(), 3)  # Adjust based on actual number of steps created
        self.assertEqual(RecipeStep.objects.get(step_number=1).description, 'Step 1: Prepare ingredients')
        self.assertEqual(RecipeStep.objects.get(step_number=2).description, 'Step 2: Cook for 30 minutes')
        self.assertEqual(RecipeStep.objects.get(step_number=3).description, 'Step 3: Serve hot')


    def test_update_recipe(self):
        recipe = RecipeFactory(user=self.user)
        ingredient = IngredientFactory(ingredient_name='pressure')
        recipe_ingredient = RecipeIngredientFactory(recipe=recipe, ingredient=ingredient)
        recipe_step = RecipeStepFactory(recipe=recipe)

        data = {
            'title': 'Updated Recipe',
            'prep_time': 45,
            'diff_lvl': 'Intermediate',
            'title_img': self.title_image,
            'ingredients[0]id': recipe_ingredient.id,
            'ingredients[0]ingredient_name': 'Updated Ingredient',
            'ingredients[0]amount': 2,
            'ingredients[0]measure': 'cups',
            'steps[0]id': recipe_step.id,
            'steps[0]step_number': 1,
            'steps[0]description': 'Updated Step',
            'steps[0]step_img': self.step_image,
            'steps[1]step_number': 2,
            'steps[1]description': 'New Step',
        }

        response = self.client.patch(reverse('recipe-detail', kwargs={'pk': recipe.pk}), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify updated recipe
        updated_recipe = Recipe.objects.get(pk=recipe.pk)
        self.assertEqual(updated_recipe.title, 'Updated Recipe')
        self.assertEqual(updated_recipe.prep_time, 45)
        self.assertEqual(updated_recipe.diff_lvl, 'Intermediate')

        # Verify updated recipe ingredient
        updated_recipe_ingredient = RecipeIngredient.objects.get(pk=recipe_ingredient.pk)
        self.assertEqual(updated_recipe_ingredient.amount, 2)
        self.assertEqual(updated_recipe_ingredient.measure, 'cups')

        # Verify updated step and new step creation
        updated_step = RecipeStep.objects.get(pk=recipe_step.pk)
        self.assertEqual(updated_step.description, 'Updated Step')

        new_step = RecipeStep.objects.get(recipe=updated_recipe, step_number=2)
        self.assertEqual(new_step.description, 'New Step')
