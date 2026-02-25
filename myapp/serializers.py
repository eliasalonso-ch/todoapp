from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Task

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class TaskSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'completed', 'created_at', 'user']