from rest_framework.generics import RetrieveUpdateAPIView
from .models import CustomUser
from .serializers import UserSerializer

class UserDetailsView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
