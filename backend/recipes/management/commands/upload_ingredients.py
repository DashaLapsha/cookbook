import csv
from django.core.management.base import BaseCommand
from recipes.models import Ingredient
from django.db import transaction

class Command(BaseCommand):
    help = 'Upload ingredients from a CSV file'

    def handle(self, *args, **kwargs):

        processed_ingredients = set()

        csv_file = 'media/data/ingredients.csv'
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                ingredient_name = row[0]
                if ingredient_name not in processed_ingredients:
                    ingredient = Ingredient(ingredient_name=ingredient_name)
                    ingredient.save()
                    processed_ingredients.add(ingredient_name)
                else:
                    print(f"Ingredient '{ingredient_name}' is already in the database.")
        transaction.commit()
