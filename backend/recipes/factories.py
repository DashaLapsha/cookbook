import factory
from .models import Ingredient, RecipeIngredient, RecipeStep, Recipe
from authn.factories import UserFactory
from django.core.files.uploadedfile import SimpleUploadedFile

class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ingredient

    ingredient_name = factory.Sequence(lambda n: f"ingredient{n}")

class RecipeIngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RecipeIngredient

    ingredient_name = factory.Sequence(lambda n: f"ingredient{n}")
    amount = factory.Faker('random_int')
    measure = factory.Faker('word')

    @factory.post_generation
    def create_ingredient(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # Create RecipeIngredient with the provided Ingredient instance
            self.ingredient = extracted
        else:
            # Create a new Ingredient instance and associate it with RecipeIngredient
            self.ingredient = IngredientFactory()


class RecipeStepFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RecipeStep
    step_img = SimpleUploadedFile("step_img.jpg", b"file_content", content_type="image/jpeg")
    step_number = factory.Faker('random_int')
    description = factory.Faker('sentence')

class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recipe

    user = factory.SubFactory(UserFactory)
    title_img = SimpleUploadedFile("step_img.jpg", b"file_content", content_type="image/jpeg")
    title = factory.Faker('sentence')
    prep_time = factory.Faker('random_int')
    diff_lvl = factory.Iterator(['Easy', 'Intermediate', 'Difficult'])