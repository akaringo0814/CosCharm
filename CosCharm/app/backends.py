from typing import Any
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest
from app.models import User
from django.contrib.auth import get_user_model


class UserAuthBackend(BaseBackend):
    def authenticate(self, request,email, password):
        try:
            user= User.objects.get(email=email)
            if user.check_password(password):
                return user 
        except User.DoesNotExist:
            return None
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
        
User = get_user_model()

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 認証ロジック
        pass

    def get_user(self, user_id):
        # ユーザー取得ロジック
        pass
