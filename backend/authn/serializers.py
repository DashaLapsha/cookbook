from rest_framework import serializers
from django.contrib.auth import get_user_model
from recipes.models import Recipe

User = get_user_model()

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    recipes = RecipeSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'profile_img', 'recipes', 'cooking_skill_lvl']

class UserOwnerSerializer(serializers.ModelSerializer):
    recipes = RecipeSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'profile_img', 'recipes', 'cooking_skill_lvl']
        extra_kwargs = {
            'email': {'required': False}, 
        }

    def update(self, instance, validated_data):
        profile_img = validated_data.pop('profile_img', None)
        if profile_img:
            instance.profile_img = profile_img
        return super().update(instance, validated_data)
