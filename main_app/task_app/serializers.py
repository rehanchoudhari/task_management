from rest_framework import serializers
from .models import Projects, Task, Attachment, COMPLETED, NOT_COMPLETED
from user_app.models import Profile, MANAGER
from datetime import datetime


class ProjectsSerializer(serializers.ModelSerializer):

    tasks = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='task-detail', source='lists')
    def create(self, validated_data):
        role = self.context['request'].user.profile.role
        created_by = self.context['request'].user.profile
        if role != MANAGER:
            raise serializers.ValidationError({'info': 'You not have a permission to create projects'})
        project = Projects.objects.create(**validated_data)
        project.created_by = created_by
        project.save()
        return project
    
    def update(self, instance, validated_data):
        role = self.context['request'].user.profile.role
        current_datetime = datetime.now()
        validated_data['updated_at'] = current_datetime
        if role != MANAGER:
            raise serializers.ValidationError({'info': 'You not have a permission to create projects'})
        return super(ProjectsSerializer, self).update(instance, validated_data)
        

    class Meta:
        model = Projects
        fields = ['url', 'id', 'project_name', 'project_description', 'created_by',
                  'total_task_count', 'completed_task_count', 'not_completed_task_count',
                  'created_at', 'updated_at', 'status', 'tasks']
        
        read_only_fields = ['updated_at', 'created_by', 'total_task_count', 'completed_task_count',
                            'not_completed_task_count']
        

class TaskSerializer(serializers.ModelSerializer):

    created_by = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='profile-detail')
    attachments = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='attachment-detail')
    def __init__(self, *args, **kwargs):
        super(TaskSerializer, self).__init__(*args, **kwargs)
        request_method = self.context['request'].method
        if request_method in ['PUT', 'PATCH']:
            role = self.context['request'].user.profile.role
            if role != MANAGER:
                self.fields.pop('assign_to')
                self.fields.pop('project_id')

    def validate(self, data):
        request_method = self.context['request'].method
        if request_method == 'POST':
            task_summary = data.get('task_summary')
            if not task_summary:
                raise serializers.ValidationError({'info': 'Task summary required fields'})
        elif request_method in ['PUT', 'PATCH']:
            if data.get('created_by'):
                raise serializers.ValidationError({'info': 'You not have permission to change created_by field'})
        return data

    def create(self, validated_data):
        request = self.context['request'].user.profile
        role = self.context['request'].user.profile.role
        if role != MANAGER:
            raise serializers.ValidationError({'info': 'You not have a permission to create Tasks'})
        project_details = validated_data.get('project_id')
        project = Projects.objects.get(id=project_details.id)
        project.total_task_count += 1
        project.not_completed_task_count += 1
        project.save()
        validated_data['created_by'] = request
        validated_data['updated_by'] = request
        task = Task.objects.create(**validated_data)
        task.save()
        return task
    
    def update(self, instance, validated_data):
        user = self.context['request'].user.profile
        current_datetime = datetime.now()
        validated_data['updated_at'] = current_datetime
        validated_data['updated_by'] = user
        task_id = self.context['view'].kwargs.get('pk')
        task_detail = Task.objects.filter(id=task_id).values('status', 'project_id')
        project = Projects.objects.get(id=task_detail[0].get('project_id'))
        current_status = task_detail[0].get('status')
        current_project_id = task_detail[0].get('project_id')
        if validated_data.get('project_id') and current_project_id != validated_data['project_id'].id:
                print('coming in ')
                project_details = validated_data.get('project_id')
                current_project = Projects.objects.get(id=project_details.id)
                project.total_task_count += 1
                current_project.total_task_count -= 1
                if current_status == COMPLETED:
                    current_project.completed_task_count -= 1
                else:
                    current_project.not_completed_task_count -= 1
                if validated_data['status'] == COMPLETED:
                    project.completed_task_count += 1
                else:
                    project.not_completed_task_count += 1
                current_project.save()
        elif current_status == validated_data['status']:
            pass
        elif validated_data['status'] == COMPLETED:
            project.not_completed_task_count -= 1
            project.completed_task_count += 1
        else:
            project.not_completed_task_count += 1
            project.completed_task_count -= 1
        project.save()
        return super(TaskSerializer, self).update(instance, validated_data)


    class Meta:
        model = Task
        fields = ['url', 'id', 'task_summary', 'project_id', 'comment', 'created_by', 'updated_by', 'assign_to',
                  'created_at', 'updated_at', 'priority', 'status', 'due_date', 'attachments']
        
        read_only_fields = ['created_by', 'updated_by', 'updated_at']


class AttachmentSerializer(serializers.ModelSerializer):

    task = serializers.HyperlinkedRelatedField(queryset=Task.objects.all(), many=False, view_name='task-detail')
    class Meta:
        model = Attachment
        fields = ['url', 'id', 'created_at', 'file', 'task']
        read_only_fields = ['created_at']
