from django.http import HttpResponse
import jwt , datetime
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from .models import User
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import login 

# Create your views here.

def hello_world(request):
    return HttpResponse("Hello, World!")

class register(APIView):
    def post(self , request):
        serializer = UserSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class Login(APIView):
    def post(self , request):
        password = request.data['password']
        email = request.data['email']
        
        print("Login Request : " , password , email)

        user = User.objects.filter(email = email).first()
        if user is None:
            raise AuthenticationFailed("user not found")
        if not user.check_password(password):
            raise AuthenticationFailed("incorrect password")
        
        login(request, user)

        payload = {
            'id' : user.user_id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token1 =  jwt.encode(payload  , 'secret' , algorithm='HS256')
        
        response = Response()
        response.set_cookie(key='jwt' , value=token1 , httponly=True)
        response.data = {
            'jwt' :token1
        }
        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("anuthenticated")
        try:
            payload = jwt.decode(token , 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')

        print(payload['id'])
        user = User.objects.filter(user_id = payload['id']).first()
        
        if not user:
            raise AuthenticationFailed('User not found')  
        serializer = UserSerializer(user)  
        return Response(serializer.data)
    
class LogoutView(APIView):
    def post(self , request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response