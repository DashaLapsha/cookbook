from rest_framework import serializers
from .models import Ingredient, RecipeIngredient, RecipeStep, Recipe
from drf_writable_nested.serializers import WritableNestedModelSerializer

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'ingredient_name']

class RecipeIngredientSerializer(WritableNestedModelSerializer):
    ingredient = IngredientSerializer()
    id = serializers.IntegerField(required=False)

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'amount', 'measure']
        extra_kwargs = {'recipe': {'required': False}}

    def create(self, validated_data):
        ingredient_data = validated_data.pop('ingredient')
        ingredient, _ = Ingredient.objects.get_or_create(ingredient_name=ingredient_data['ingredient_name'].lower())
        recipe = self.context['recipe']
        recipe_ingredient = RecipeIngredient.objects.create(ingredient=ingredient, recipe=recipe, **validated_data)
        return recipe_ingredient
    
    def update(self, instance, validated_data):
        ingredient_data = validated_data.pop('ingredient')
        ingredient, _ = Ingredient.objects.get_or_create(ingredient_name=ingredient_data['ingredient_name'].lower())
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

class RecipeSerializer(WritableNestedModelSerializer):
        user = serializers.HiddenField(default=serializers.CurrentUserDefault())
        ingredients = RecipeIngredientSerializer(many=True)
        steps = RecipeStepSerializer(many=True)
    
        class Meta:
            model = Recipe
            fields = '__all__'
    
        def create(self, validated_data):
            ingredients_data = validated_data.pop('ingredients', [])
            steps_data = validated_data.pop('steps', [])
        
            recipe = Recipe.objects.create(**validated_data)
        
            for ingredient_data in ingredients_data:
                ingredient_data['recipe'] = recipe
                ingredient_serializer = RecipeIngredientSerializer(data=ingredient_data, context={'recipe': recipe})
                if ingredient_serializer.is_valid():
                    ingredient_serializer.save()
        
            for step_data in steps_data:
                step_data['recipe'] = recipe
                step_serializer = RecipeStepSerializer(data=step_data, context={'recipe': recipe})
                if step_serializer.is_valid():
                    step_serializer.save()
        
            return recipe
    
        def update(self, instance, validated_data):
            ingredients_data = validated_data.pop('ingredients', [])
            steps_data = validated_data.pop('steps', [])
        
            instance.title = validated_data.get('title', instance.title)
            instance.prep_time = validated_data.get('prep_time', instance.prep_time)
            instance.diff_lvl = validated_data.get('diff_lvl', instance.diff_lvl)
            instance.title_img = validated_data.get('title_img', instance.title_img)
            instance.save()
        
            for ingredient_data in ingredients_data:
                ingredient_id = ingredient_data.get('id')
                if ingredient_id:
                    ingredient = RecipeIngredient.objects.get(id=ingredient_id, recipe=instance)
                    ingredient_serializer = RecipeIngredientSerializer(instance=ingredient, data=ingredient_data, context={'recipe': instance}, partial=True)
                else:
                    ingredient_serializer = RecipeIngredientSerializer(data=ingredient_data, context={'recipe': instance})
                if ingredient_serializer.is_valid():
                    ingredient_serializer.save()
        
            for step_data in steps_data:
                step_id = step_data.get('id')
                if step_id:
                    step = RecipeStep.objects.get(id=step_id, recipe=instance)
                    step_serializer = RecipeStepSerializer(instance=step, data=step_data, context={'recipe': instance}, partial=True)
                else:
                    step_serializer = RecipeStepSerializer(data=step_data, context={'recipe': instance})
                if step_serializer.is_valid():
                    step_serializer.save()
        
            instance.ingredients.exclude(id__in=[item['id'] for item in ingredients_data if 'id' in item]).delete()
            instance.steps.exclude(id__in=[item['id'] for item in steps_data if 'id' in item]).delete()
        
            return instance