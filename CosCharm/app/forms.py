from django import forms
from django.contrib.auth.forms import UserCreationForm
from app.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import MyMake, MyCosmetic


class Signupform(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("このメールアドレスは既に登録されています")
        return email 
    
#class LoginForm(forms.Form):
    #email = forms.EmailField()
    #password = forms.CharField()

class LoginForm(AuthenticationForm): 
    username = forms.CharField(max_length=254, required=True) 
    password = forms.CharField(widget=forms.PasswordInput, required=True)

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
class MyCosmeticForm(forms.ModelForm):
    class Meta:
        model = MyCosmetic
        fields = ['name', 'used_in_make']
