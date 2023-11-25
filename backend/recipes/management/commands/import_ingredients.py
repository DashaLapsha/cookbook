import csv
from django.core.management.base import BaseCommand
from recipes.models import Ingredient

class Command(BaseCommand):
    help = 'Import ingredients from a CSV file'

    def handle(self, *args, **kwargs):
        csv_file_path = 'media/data/ingredients.csv'

        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)

            for row in csv_reader:
                ingredient_name = row[0].strip()
                Ingredient.objects.get_or_create(ingredient_name=ingredient_name)

        self.stdout.write(self.style.SUCCESS('Ingredients imported successfully.'))