from django.test import TestCase , Client
from ecommerceapp.models import User, Role
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ecommerceapp.serializers import UserSerializer

# Create your tests here.

class HelloWorldViewTest(TestCase):
    def test_hello_world_view(self):

        url = reverse('hello_world')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello, World!")
        
        
class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register-view')

        # Create a test role
        self.role = Role.objects.create(role_name='TestRole')

        # Define test user data
        self.user_data = {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'role': self.role.role_id,
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the user was created in the database
        user = User.objects.filter(email=self.user_data['email']).first()
        self.assertIsNotNone(user)

        # Check if the user's data matches the submitted data
        serializer = UserSerializer(user)
        self.assertEqual(serializer.data['name'], self.user_data['name'])

    
class UserViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            name="Test User",
            email="test@example.com",
            password="testpassword",
            role=Role.objects.create(role_name='TestRole')
        )

    def test_user_view_authenticated(self):
        print("Testing user view authenticated")
        # Log in
        login_url = reverse('login-view')
        login_data = {
            'email': self.user.email,
            'password': self.user.password,
        }

        print("user-data:", self.user.email, ":", self.user.password)
        print("login:", login_data)

        response = self.client.post(login_url, login_data, format='json')
        print("response:", response.status_code)
        print("response.data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        jwt_token = response.data['jwt']
        
        # Set the JWT token in the client's cookies
        self.client.cookies['jwt'] = jwt_token

        # Make a GET request to the user view
        user_view_url = reverse('user-view')
        response = self.client.get(user_view_url)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the serialized user data matches the user's data
        serializer = UserSerializer(self.user)
        self.assertEqual(response.data, serializer.data)

    def test_user_view_unauthenticated(self):
        # Make a GET request to the user view without authenticating
        user_view_url = reverse('user-view')
        response = self.client.get(user_view_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Add more test cases as needed for edge cases and err
            