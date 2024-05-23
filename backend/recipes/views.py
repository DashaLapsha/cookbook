from rest_framework import viewsets, permissions, status
from .models import Recipe
from .serializers import RecipeSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
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

    def create(self, request, *args, **kwargs):
        print('da')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Save title_img if provided in a multipart request
        title_img = request.FILES.get('title_img', None)
        if title_img:
            recipe.title_img = title_img
            recipe.save()

        return Response(self.get_response_data(recipe), status=201, headers=headers)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     recipe = self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)

    #     title_img = request.FILES.get('title_img', None)
    #     if title_img:
    #         recipe.title_img = title_img
    #         recipe.save()

    #     return Response(self.get_response(recipe), status=201, headers=headers)