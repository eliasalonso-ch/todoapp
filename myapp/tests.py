from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model


class RegisterTestCase(APITestCase):
    def test_successful_registration(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post('/api/v1/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_missing_password(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com'
        }
        response = self.client.post('/api/v1/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_username(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        self.client.post('/api/v1/register/', data)
        response = self.client.post('/api/v1/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

User = get_user_model()

class TaskTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        response = self.client.post('/api/v1/token/', {'username': 'testuser', 'password': 'testpassword123'})
        token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_create_task(self):
        data = {
            'title': 'Test Task',
            'description': 'This is a test task.',
            'completed': False
        }
        response = self.client.post('/api/v1/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_tasks(self):
        response = self.client.get('/api/v1/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_access_others_tasks(self):
    
        other_user = User.objects.create_user(username='otheruser', password='otherpassword123')
        other_client = APIClient()
        response = other_client.post('/api/v1/token/', {'username': 'otheruser', 'password': 'otherpassword123'})
        other_client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')
    
        other_client.post('/api/v1/tasks/', {'title': 'Other User Task'})
    
        response = self.client.get('/api/v1/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_weak_password(self):
        data = {
        'username': 'testuser',
        'password': 'a'
    }
        response = self.client.post('/api/v1/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class HealthCheckTestCase(APITestCase):
    def test_health_check(self):
        response = self.client.get('/api/v1/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'ok')
        self.assertEqual(response.data['database'], 'ok')