from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # 削除したフィールド
    first_name = None
    last_name = None
    date_joined = None
    groups = None
    user_permissions = None

    # 独自フィールド
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # 統合されたProfileのフィールド
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[('男性', '男性'), ('女性', '女性')],
        blank=True
    )
    skin_type = models.CharField(
        max_length=10,
        choices=[('乾燥肌', '乾燥肌'), ('脂性肌', '脂性肌'), ('普通肌', '普通肌'), ('混合肌', '混合肌'), ('不明', '不明')],
        blank=True,
        null=True,
        verbose_name="肌質"
    )
    personal_color = models.CharField(
        max_length=10,
        choices=[('イエベ春', 'イエベ春'), ('ブルベ夏', 'ブルベ夏'), ('イエベ秋', 'イエベ秋'), ('ブルベ冬', 'ブルベ冬'), ('不明', '不明')],
        blank=True,
        null=True,
        verbose_name="パーソナルカラー"
    )
    #profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True, )  # defaultを設定

    # マネージャー
    objects = UserManager()

    # ユーザー名やメールの設定
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]  # 必須項目

    class Meta:
        db_table = "users"


class MyMake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='makes')
    make_name = models.CharField(max_length=100)
    make_memo = models.CharField(max_length=255, default="")
    image = models.ImageField(upload_to='make_images/')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    cosmetics = models.ManyToManyField('CosmeticMaster', through='MyMakeCosmetic', related_name='my_makes')

class MyMakeCosmetic(models.Model):
    my_make = models.ForeignKey(MyMake, on_delete=models.CASCADE, related_name='my_make_cosmetics')
    cosmetic = models.ForeignKey('CosmeticMaster', on_delete=models.CASCADE, related_name='cosmetic_my_makes')
    is_main = models.BooleanField(default=False)  # メインコスメかどうか

class CosmeticMaster(models.Model):
    """コスメマスター"""
    cosmetic_name = models.CharField(max_length=100, verbose_name="商品名", null=True)
    brand = models.CharField(max_length=100, verbose_name="ブランド名")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="価格")
    #photo = models.ImageField(upload_to='cosmetics/', blank=True, null=True, verbose_name="画像")
    photo = models.CharField(max_length=100, blank=True, null=True, verbose_name="画像のパス")
    #photo = models.CharField(max_length=255, null=True, blank=True)
    CATEGORY_CHOICES = [
        (0, 'フェイスケア'),
        (1, 'ポイントメイク'),
        (2, 'ベースメイク')
    ]
    SUB_CATEGORY_CHOICES = [
    # フェイスケア
    (0, '化粧水'),
    (1, '乳液'),
    (2, '美容液'),
    
    # ポイントメイク
    (3, 'アイブロウ'),
    (4, 'アイライナー'),
    (5, 'アイシャドウ'),
    (6, 'マスカラ'),
    (7, 'チーク'),
    (8, 'リップ'),
    
    # ベースメイク
    (9, '下地'),
    (10, 'ファンデーション'),
    (11, 'フェイスパウダー')
]

    category = models.IntegerField(choices=CATEGORY_CHOICES, verbose_name="カテゴリ")
    sub_category = models.IntegerField(choices=SUB_CATEGORY_CHOICES, verbose_name="サブカテゴリ",default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日", null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日", null=True)

    def __str__(self):
        return f"{self.brand} - {self.cosmetic_name}"  # 修正: name -> cosmetic_name



class MyCosmetic(models.Model):
    """マイコスメ"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cosmetics', verbose_name="ユーザー")
    cosmetic = models.ForeignKey(CosmeticMaster, on_delete=models.CASCADE, verbose_name="コスメ")
    used_in_make = models.BooleanField(default=False, verbose_name="メイクに使用")
    is_favorite = models.BooleanField(default=False, verbose_name="お気に入り")

    USAGE_STATUS_CHOICES = [
        ('not_used', '未使用'),
        ('in_use', '使用中'),
        ('used', '使用済み'),
    ]
    usage_status = models.CharField(
        max_length=20,
        choices=USAGE_STATUS_CHOICES,
        default='not_used',
        verbose_name="使用ステータス"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日", null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日", null=True)
    is_deleted = models.BooleanField(default=False, verbose_name="削除済み")

    def __str__(self):
        return f"{self.user.username} - {self.cosmetic.brand} - {self.cosmetic.cosmetic_name}"

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    my_make = models.ForeignKey(MyMake, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'my_make')


# フォローモデル
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # 重複フォローを防ぐ



