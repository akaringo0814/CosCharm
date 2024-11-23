from django import forms
from django.contrib.auth.forms import UserCreationForm
from app.models import User
from django.contrib.auth import authenticate
from .models import MyMake, MyCosme


class Signupform(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("このメールアドレスは既に登録されています")
        return email 
    
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        print (email,password)
        self.user = authenticate(email=email, password=password)
        if self.user is None:
            raise forms.ValidationError("認証に失敗しました")
        return self.cleaned_data


# MyMake用フォーム
class MyMakeForm(forms.ModelForm):
    class Meta:
        model = MyMake
        fields = ['make_name', 'image']  # 必要なフィールドを指定

# MyCosme用フォーム
class MyCosmeForm(forms.ModelForm):
    class Meta:
        model = MyCosme
        fields = ['name', 'used_in_make']
