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
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False)


    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"] #必須項目


    class Meta:
        db_table = "users"

 

class MyMake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='makes')
    make_name = models.CharField(max_length=100)
    make_memo =models.TextField
    image = models.ImageField(upload_to='make_images/')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    
class CosmeticMaster(models.Model):
    """コスメマスター"""
    cosmetic_name = models.CharField(max_length=100, verbose_name="商品名", null=True)
    brand = models.CharField(max_length=100, verbose_name="ブランド名")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="価格")
    photo = models.ImageField(upload_to='cosmetics/', blank=True, null=True, verbose_name="画像")

    CATEGORY_CHOICES = [
        (0, 'フェイスケア'),
        (1, 'ポイントメイク'),
        (2, 'ベースメイク')
    ]
    category = models.IntegerField(choices=CATEGORY_CHOICES, verbose_name="カテゴリ")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日", null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日", null=True)

    def __str__(self):
        return f"{self.brand} - {self.name}"


class MyCosmetic(models.Model):
    """マイコスメ"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cosmetics', verbose_name="ユーザー")
    cosmetic = models.ForeignKey(CosmeticMaster, on_delete=models.CASCADE, verbose_name="コスメ")
    used_in_make = models.BooleanField(default=False, verbose_name="メイクに使用")
    is_favorite = models.BooleanField(default=False, verbose_name="お気に入り")
    status = models.CharField(
        max_length=10,
        choices=[
            ('未使用', '未使用'),
            ('使用中', '使用中'),
            ('使用済み', '使用済み')
        ],
        default='未使用',
        verbose_name="使用ステータス"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日", null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日", null=True)
    def __str__(self):
        return f"{self.user.username} - {self.cosmetic.brand} - {self.cosmetic.cosmetic_name}"
