from rest_framework import viewsets, permissions, status
from .models import Recipe
from .serializers import RecipeSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

class IsRecipeOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(obj, Recipe):
            return obj.user == request.user or request.user.is_staff
        if hasattr(obj, 'recipe'):
            return obj.recipe.user == request.user or request.user.is_staff
        return False

class BaseRecipePermissionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [permissions.IsAuthenticated]
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsRecipeOwnerOrAdmin]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

class RecipeViewSet(BaseRecipePermissionViewSet):
    queryset = Recipe.objects.all().order_by('-id')
    serializer_class = RecipeSerializer
    parser_classes = (MultiPartParser, FormParser)

# class IngredientViewSet(BaseRecipePermissionViewSet):
#     queryset = Ingredient.objects.all()
#     serializer_class = IngredientSerializer

# class RecipeIngredientViewSet(BaseRecipePermissionViewSet):
#     queryset = RecipeIngredient.objects.all()
#     serializer_class = RecipeIngredientSerializer

# class RecipeStepViewSet(BaseRecipePermissionViewSet):
#     queryset = RecipeStep.objects.all()
#     serializer_class = RecipeStepSerializer
