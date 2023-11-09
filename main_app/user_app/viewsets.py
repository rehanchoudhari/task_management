from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer, ProfileSerializer
from .permissions import UserPermission, ProfilePermission
from .models import Profile



class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [UserPermission, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [ProfilePermission]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer