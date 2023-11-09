from rest_framework import viewsets, filters
from .models import Projects, Task, Attachment
from .serializers import ProjectsSerializer, TaskSerializer, AttachmentSerializer
from .permissions import ProjectPermission, TaskPermission, AttachmentPermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend


class ProjectsViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [ProjectPermission, ]
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['project_name', 'description']
    filterset_fields = ['status']


class TaskViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [TaskPermission, ]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['task_summary', 'comment']
    filterset_fields = ['status', 'priority', 'created_by', 'updated_by', 'assign_to']


class AttachmentViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [AttachmentPermission, ]
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['file']