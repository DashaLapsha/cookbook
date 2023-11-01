from django.db import models
from django.conf import settings

class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Intermediate', 'Intermediate'),
        ('Difficult', 'Difficult'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    cooking_instructions = models.TextField()
    prep_time = models.PositiveIntegerField()
    diff_lvl = models.CharField(max_length=15, choices=DIFFICULTY_CHOICES)
    title_img = models.ImageField(upload_to='media/recipe_images/')
    # other_requirements = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title



class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=100)

    def __str__(self):
        return self.ingredient_name



class UnwantedIngredient(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.ingredient.ingredient_name}"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    measure = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.recipe.title} - {self.ingredient.ingredient_name}"
