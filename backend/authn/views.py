from rest_framework.generics import RetrieveUpdateAPIView
from .models import CustomUser
from .serializers import UserSerializer, UserOwnerSerializer
from rest_framework.response import Response
from dj_rest_auth.views import LoginView as DefaultLoginView
from dj_rest_auth.views import LogoutView as DefaultLogoutView
from rest_framework.views import APIView
from django.middleware.csrf import get_token
from rest_framework.permissions import IsAuthenticated
from dj_rest_auth.registration.views import RegisterView as DefaultRegisterView
from rest_framework.parsers import MultiPartParser
from rest_framework.views import status

class CustomRegisterView(DefaultRegisterView):
    parser_classes = [MultiPartParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Handle profile image upload
        profile_img = request.FILES.get('profile_img', None)
        if profile_img:
            user.profile_img = profile_img
            user.save()

        return Response(self.get_response_data(user), status=201, headers=headers)

class CSRFTokenView(APIView):
    def get(self, request, *args, **kwargs):
        csrf_token = get_token(request)
        return Response({'csrfToken': csrf_token})

class UserDetailsView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.user.id == int(self.kwargs['id']):
            return UserOwnerSerializer
        else:
            return UserSerializer
        
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class CustomLoginView(DefaultLoginView):
    def get_response(self):
        response = super().get_response()
        if response.status_code == 200:
            user = self.user
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
            response.data['user'] = user_data
        return response

class CustomLogoutView(DefaultLogoutView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
