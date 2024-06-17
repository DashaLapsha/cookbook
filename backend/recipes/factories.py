import factory
from django.contrib.auth import get_user_model
from .models import Ingredient, Recipe, RecipeIngredient, RecipeStep
from django.core.files.uploadedfile import SimpleUploadedFile
import io
from PIL import Image, ImageDraw

import io
from PIL import Image, ImageDraw

def create_image():
    image = Image.new('RGB', (100, 100), color='white')
    draw = ImageDraw.Draw(image)
    draw.line((0, 0) + image.size, fill='black')

    image_buffer = io.BytesIO()
    image.save(image_buffer, format='PNG')
    
    return SimpleUploadedFile('test_image.png', image_buffer.read(), content_type='image/png')


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password')

class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ingredient

    ingredient_name = factory.Faker('word')

class RecipeIngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RecipeIngredient

    ingredient = factory.SubFactory(IngredientFactory)
    amount = factory.Faker('random_int', min=1, max=10)
    measure = factory.Faker('word')

class RecipeStepFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RecipeStep

    step_number = factory.Sequence(lambda n: n + 1)
    description = factory.Faker('sentence')
    step_img = factory.LazyFunction(lambda: SimpleUploadedFile('step_image.png', create_image().read()))

class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recipe

    user = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence')
    prep_time = factory.Faker('random_int', min=1, max=120)
    diff_lvl = factory.Faker('random_element', elements=[choice[0] for choice in Recipe.DIFFICULTY_CHOICES])
    title_img = factory.LazyFunction(lambda: SimpleUploadedFile('title_image.png', create_image().read()))
