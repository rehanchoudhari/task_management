from .models import Projects, Task, COMPLETED, NOT_COMPLETED
from django.db.models import Count, Q
from rest_framework.views import APIView
from rest_framework.response import Response

class TaskCompletionReport(APIView):
    def get(self, request):
        completed_tasks = Task.objects.filter(status=COMPLETED).count()
        pending_tasks = Task.objects.filter(status=NOT_COMPLETED).count()
        Total_tasks = Task.objects.all().count()
        user_activity = Task.objects.values('created_by').annotate(total_task=Count('id'))

        return Response({
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'overdue_tasks': Total_tasks,
            'user_activity': list(user_activity)
        })
    
# class SpendTimeOnEachTask(APIView):
#     def get(self, request):
