from rest_framework import viewsets, permissions
from .models import Recipe, RecipeIngredient, RecipeStep, Ingredient
from .serializers import RecipeSerializer, RecipeIngredientSerializer, RecipeStepSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import generics
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
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class RecipeIngredientListView(generics.ListAPIView):
    serializer_class = RecipeIngredientSerializer

    def get_queryset(self):
        recipe_pk = self.kwargs['recipe_pk']
        return RecipeIngredient.objects.filter(recipe_id=recipe_pk)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RecipeStepListView(generics.ListAPIView):
    serializer_class = RecipeStepSerializer

    def get_queryset(self):
        recipe_pk = self.kwargs['recipe_pk']
        return RecipeStep.objects.filter(recipe_id=recipe_pk)