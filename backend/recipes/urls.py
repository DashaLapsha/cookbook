from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet, RecipeIngredientListView, RecipeStepListView

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipe')

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:recipe_pk>/ingredients/', RecipeIngredientListView.as_view(), name='recipe-ingredients'),
    path('recipes/<int:recipe_pk>/steps/', RecipeStepListView.as_view(), name='recipe-steps'),
]
