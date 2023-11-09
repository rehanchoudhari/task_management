from django.contrib import admin
from .models import Projects, Task, Attachment

# Register your models here.


class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = []


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = []

class AttachmentAdmin(admin.ModelAdmin):
    readonly_fields = []

admin.site.register(Projects, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Attachment, AttachmentAdmin)