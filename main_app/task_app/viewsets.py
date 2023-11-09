from rest_framework import viewsets
from .models import Projects, Task, Attachment
from .serializers import ProjectsSerializer, TaskSerializer, AttachmentSerializer
from .permissions import ProjectPermission, TaskPermission, AttachmentPermission
from rest_framework_simplejwt.authentication import JWTAuthentication


class ProjectsViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [ProjectPermission, ]
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer


class TaskViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [TaskPermission, ]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class AttachmentViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [AttachmentPermission, ]
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer