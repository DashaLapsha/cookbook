from rest_framework import serializers
from django.db import transaction
from .models import Recipe, RecipeIngredient, RecipeStep, Ingredient

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    ingredient_name = serializers.CharField()

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient_name', 'amount', 'measure']
        extra_kwargs = {'recipe': {'required': False}}

    def create(self, validated_data):
        ingredient_name = validated_data.pop('ingredient_name')
        ingredient, _ = Ingredient.objects.get_or_create(ingredient_name=ingredient_name.lower())
        recipe = self.context['recipe']
        recipe_ingredient = RecipeIngredient.objects.create(ingredient=ingredient, recipe=recipe, **validated_data)
        return recipe_ingredient

    def update(self, instance, validated_data):
        ingredient_name = validated_data.pop('ingredient_name')
        ingredient, _ = Ingredient.objects.get_or_create(ingredient_name=ingredient_name.lower())
        instance.ingredient = ingredient
        instance.amount = validated_data.get('amount', instance.amount)
        instance.measure = validated_data.get('measure', instance.measure)
        instance.save()
        return instance

class RecipeStepSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = RecipeStep
        fields = ['id', 'step_number', 'description', 'step_img']
        extra_kwargs = {'recipe': {'required': False}}

    def create(self, validated_data):
        recipe = self.context['recipe']
        recipe_step = RecipeStep.objects.create(recipe=recipe, **validated_data)
        return recipe_step

    def update(self, instance, validated_data):
        instance.step_number = validated_data.get('step_number', instance.step_number)
        instance.description = validated_data.get('description', instance.description)
        instance.step_img = validated_data.get('step_img', instance.step_img)
        instance.save()
        return instance

class RecipeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    ingredients = RecipeIngredientSerializer(many=True)
    steps = RecipeStepSerializer(many=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        steps_data = validated_data.pop('steps', [])
        print(f"Validated data: {validated_data}")

        with transaction.atomic():
            recipe = Recipe.objects.create(**validated_data)

            for ingredient_data in ingredients_data:
                ingredient_serializer = RecipeIngredientSerializer(data=ingredient_data, context={'recipe': recipe})
                ingredient_serializer.is_valid(raise_exception=True)
                ingredient_serializer.save()

            for step_data in steps_data:
                step_serializer = RecipeStepSerializer(data=step_data, context={'recipe': recipe})
                step_serializer.is_valid(raise_exception=True)
                step_serializer.save()

            return recipe

    def update(self, instance, validated_data):
        print(validated_data)
        ingredients_data = validated_data.pop('ingredients', [])
        steps_data = validated_data.pop('steps', [])

        with transaction.atomic():
            instance.title = validated_data.get('title', instance.title)
            instance.prep_time = validated_data.get('prep_time', instance.prep_time)
            instance.diff_lvl = validated_data.get('diff_lvl', instance.diff_lvl)
            instance.title_img = validated_data.get('title_img', instance.title_img)
            instance.save()

            # Handle ingredients
            for ingredient_data in ingredients_data:
                ingredient_id = ingredient_data.get('id')
                if ingredient_id:
                    ingredient_instance = RecipeIngredient.objects.get(id=ingredient_id, recipe=instance)
                    ingredient_serializer = RecipeIngredientSerializer(instance=ingredient_instance, data=ingredient_data, context={'recipe': instance}, partial=True)
                else:
                    ingredient_serializer = RecipeIngredientSerializer(data=ingredient_data, context={'recipe': instance})
                ingredient_serializer.is_valid(raise_exception=True)
                ingredient_serializer.save()

            # Handle steps
            for step_data in steps_data:
                step_id = step_data.get('id')
                if step_id:
                    step_instance = RecipeStep.objects.get(id=step_id, recipe=instance)
                    step_serializer = RecipeStepSerializer(instance=step_instance, data=step_data, context={'recipe': instance}, partial=True)
                else:
                    step_serializer = RecipeStepSerializer(data=step_data, context={'recipe': instance})
                step_serializer.is_valid(raise_exception=True)
                step_serializer.save()

            instance.ingredients.exclude(id__in=[item['id'] for item in ingredients_data if 'id' in item]).delete()
            instance.steps.exclude(id__in=[item['id'] for item in steps_data if 'id' in item]).delete()

            return instance
