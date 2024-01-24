from django.urls import path , include
from . import views
from .views import hello_world

urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
    path('register'  , views.register.as_view()  , name='register-view'),
    path('login' , views.Login.as_view() , name='login-view'),
    path('userdata' , views.UserView.as_view(), name='user-view'),
    path('logout' , views.LogoutView.as_view())
]