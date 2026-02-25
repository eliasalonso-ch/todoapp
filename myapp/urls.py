from rest_framework import routers
from .views import TaskViewSet
from rest_framework.routers import DefaultRouter
from .views import health_check
from django.urls import path

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('health/', health_check, name='health_check'),
] + router.urls