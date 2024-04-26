from django.db import models
from django.conf import settings

class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.ingredient_name

class UnwantedIngredient(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.ingredient.ingredient_name}"

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    measure = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.recipe.title} - {self.ingredient.ingredient_name}"

class RecipeStep(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    step_number = models.PositiveIntegerField()
    description = models.TextField()
    step_img = models.ImageField(upload_to='recipe_images/steps', null=True, blank=True)

    def __str__(self):
        return f"Step {self.step_number}: {self.description}"
    
class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Intermediate', 'Intermediate'),
        ('Difficult', 'Difficult'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    prep_time = models.PositiveIntegerField()
    diff_lvl = models.CharField(max_length=15, choices=DIFFICULTY_CHOICES)
    title_img = models.ImageField(upload_to='recipe_images/', null=True, blank=True)
    ingredients = models.ManyToManyField(RecipeIngredient, related_name='recipes')
    steps = models.ManyToManyField(RecipeStep, related_name='recipes')

    def __str__(self):
        return self.title




# from django.conf import settings
# from django.db import models
# from .storages import MyLocalStorage, MyRemoteStorage


# def select_storage():
#     return MyLocalStorage() if settings.DEBUG else MyRemoteStorage()


# class MyModel(models.Model):
#     my_file = models.FileField(storage=select_storage)