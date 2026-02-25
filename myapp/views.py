from django.shortcuts import render
from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    try:
        from django.db import connection
        connection.ensure_connection()
        db_status = 'ok'
    except Exception:
        db_status = 'error'
    
    return Response({
        'status': 'ok',
        'database': db_status
    })

logger = logging.getLogger(__name__)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['completed']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            logger.info(f'Tasks fetched by user {user.username}')
            return Task.objects.select_related('user').filter(user=user).order_by('-created_at')
        logger.warning('Unauthenticated user attempted to access tasks')
        return Task.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        logger.info(f'Task created by user {self.request.user.username}')
