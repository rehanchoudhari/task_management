from rest_framework import routers
from .viewsets import UserViewSet, ProfileViewSet


app_name = 'user_app'
router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('profiles', ProfileViewSet)