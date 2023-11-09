from rest_framework import permissions
from user_app.models import MANAGER


class ProjectPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        return request.user.profile == obj.created_by
    

class TaskPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user.profile.role == MANAGER:
            return True
        return request.user.profile == obj.assign_to
    

class AttachmentPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return True
        return False
    
    def has_objct_permission(self, request, view, obj):
        if request.user.profile.role == MANAGER:
            return True
        return request.user.profile == obj.task.assign_to