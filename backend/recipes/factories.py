import factory
from .models import Ingredient, RecipeIngredient, RecipeStep, Recipe
from authn.factories import UserFactory

class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ingredient

    ingredient_name = factory.Sequence(lambda n: f"ingredient{n}")

class RecipeIngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RecipeIngredient

    ingredient = factory.SubFactory(IngredientFactory)
    amount = factory.Faker('random_int')
    measure = factory.Faker('word')

class RecipeStepFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RecipeStep

    step_number = factory.Faker('random_int')
    description = factory.Faker('sentence')

class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recipe

    user = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence')
    prep_time = factory.Faker('random_int')
    diff_lvl = factory.Iterator(['Easy', 'Intermediate', 'Difficult'])