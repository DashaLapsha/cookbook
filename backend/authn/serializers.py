from rest_framework import serializers, viewsets
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'dietary_pref', 'cooking_skill_lvl')