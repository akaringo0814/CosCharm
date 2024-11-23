from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
# Create your models here.



class User(AbstractUser):
    first_name = None
    last_name = None
    date_joined = None
    groups = None
    user_permissions = None


    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"] #必須項目


    class Meta:
        db_table = "users"
 

class MyMake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='makes')
    make_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='make_images/')
    created_at = models.DateTimeField(auto_now_add=True)

class MyCosme(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cosmetics')
    name = models.CharField(max_length=100)
    used_in_make = models.BooleanField(default=False)
