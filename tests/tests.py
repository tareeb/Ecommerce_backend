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
        print("\nSetting up the test : RegisterUser")
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
        print("Testing : RegisterUser")
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the user was created in the database
        user = User.objects.filter(email=self.user_data['email']).first()
        self.assertIsNotNone(user)

        # Check if the user's data matches the submitted data
        serializer = UserSerializer(user)
        self.assertEqual(serializer.data['name'], self.user_data['name'])
        print("Test RegisterUser : Done")

    
class UserViewTest(TestCase):
    def setUp(self):
        print("\nSetting up tests : UserLogin and JWT Token Generation ")
        self.client = Client()
        self.user = User.objects.create(
            name="Test User",
            email="test@example.com",
            password="testpassword",
            role=Role.objects.create(role_name='TestRole')
        )

    def test_user_view_authenticated(self):
        # Log in
        print("Testing UserLogin")
        login_url = reverse('login-view')
        login_data = {
            'email': self.user.email,
            'password': self.user.password,
        }

        response = self.client.post(login_url, login_data, format='json')
       
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        jwt_token = response.data['jwt']
        
        self.client.cookies['jwt'] = jwt_token

        print("User Authentication Successfull")
        print("Testing User-View : Getting data based on JWT Token from cookie")
        
        # Make a GET request to the user view
        user_view_url = reverse('user-view')
        response = self.client.get(user_view_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UserSerializer(self.user)
        self.assertEqual(response.data, serializer.data)
        
        print("Test User-View : Done")

    def test_user_view_unauthenticated(self):
        # Make a GET request to the user view without authenticating
        user_view_url = reverse('user-view')
        response = self.client.get(user_view_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        print("Test Unauthenticated User-View : Done")

            