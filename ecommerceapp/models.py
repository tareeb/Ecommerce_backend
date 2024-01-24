from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.role_name
    
    #For Ecommere store roles can be : Buyer , seller , Admin
    
class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    name  = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password  = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email

