from rest_framework import routers
from .viewsets import ProjectsViewSet, TaskViewSet, AttachmentViewSet

app_name = 'task_app'
router = routers.DefaultRouter()
router.register('projects', ProjectsViewSet)
router.register('task', TaskViewSet)
router.register('attachments', AttachmentViewSet)