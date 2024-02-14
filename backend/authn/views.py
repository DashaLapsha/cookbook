from rest_framework.generics import RetrieveUpdateAPIView
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.response import Response
from dj_rest_auth.views import LoginView as DefaultLoginView

class UserDetailsView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

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
