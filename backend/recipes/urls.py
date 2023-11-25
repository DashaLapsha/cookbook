from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet, IngredientViewSet, RecipeIngredientViewSet, RecipeStepViewSet

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'ingredients', IngredientViewSet, basename='ingredient')
router.register(r'recipe-ingredients', RecipeIngredientViewSet, basename='recipeingredient')
router.register(r'recipe-steps', RecipeStepViewSet, basename='recipestep')

urlpatterns = [
    path('', include(router.urls)),
]