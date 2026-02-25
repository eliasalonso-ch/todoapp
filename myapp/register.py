from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
import logging
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .tasks import send_welcome_email

logger = logging.getLogger(__name__)

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            logger.warning('Registration attempt with missing credentials')
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            validate_password(password)
        
        except ValidationError as e:
            logger.warning(f'Password validation error: {e.messages}')
            return Response({'error': ' '.join(e.messages)}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            logger.warning(f'Registration attempt with existing username: {username}')
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password)
        logger.info(f'New user registered: {username}')
        return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
    
        send_welcome_email.delay(username)