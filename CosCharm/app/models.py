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
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False)


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
    
class CosmeticMaster(models.Model):
    """コスメマスター"""
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='cosmetics/', blank=True, null=True)

    def __str__(self):
        return f"{self.brand} - {self.name}"

class MyCosmetic(models.Model):
    """マイコスメ"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cosmetics')
    name = models.CharField(max_length=100)
    used_in_make = models.BooleanField(default=False)
    image = models.ImageField(upload_to='cosmetics/')
    cosmetic = models.ForeignKey(CosmeticMaster, on_delete=models.CASCADE)  # 登録されたコスメ
    is_favorite = models.BooleanField(default=False)  # お気に入りフラグ
    status = models.CharField(
        max_length=10,
        choices=(
            ('未使用', '未使用'),
            ('使用中', '使用中'),
            ('使用済み', '使用済み')
        ),
        default='未使用'
    )

    def __str__(self):
        return f"{self.user.username} - {self.cosmetic.name}"
