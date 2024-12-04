from django import forms
from django.contrib.auth.forms import UserCreationForm
from app.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import MyMake, MyCosmetic, CosmeticMaster
#from .models import Profile


class Signupform(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("このメールアドレスは既に登録されています")
        return email 
    

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

#class LoginForm(AuthenticationForm):
    #email = forms.EmailField(max_length=254, required=True)  # メールアドレスを使用
    #password = forms.CharField(widget=forms.PasswordInput, required=True)  # パスワード
    #def clean(self):
        #email = self.cleaned_data.get("email")
        #password = self.cleaned_data.get("password")

        # メールアドレスを使ってユーザー認証
        #user = authenticate(request=self.request, email=email, password=password)
        
        #if user is None:
            #raise forms.ValidationError("認証に失敗しました")
        
        #self.user = user
        #return self.cleaned_data

class LoginForm(forms.Form):
    email = forms.EmailField(label="メールアドレス", max_length=254, required=True)
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user = authenticate(self.request, email=email, password=password)
        if user is None:
            raise forms.ValidationError("メールアドレスまたはパスワードが正しくありません。")
        self.user = user
        return self.cleaned_data

    def get_user(self):
        return self.user
 

# MyMake用フォーム
class MyMakeForm(forms.ModelForm):
    
    class Meta:
        model = MyMake
        fields = ['make_name', 'image']  # 必要なフィールドを指定

# MyCosme用フォーム
class MyCosmeticForm(forms.ModelForm):
    cosmetic = forms.ModelChoiceField(
        queryset=CosmeticMaster.objects.all(),
        label="商品名",
        widget=forms.Select
    )

    class Meta:
        model = MyCosmetic
        fields = ['cosmetic', 'used_in_make', 'is_favorite', 'status']

    #サブカテゴリに
    #def __init__(self, *args, **kwargs):
        #super().__init__(*args, **kwargs)
        #self.fields['facecare'].widget.attrs.update({'class': 'sub-category', 'data-category': '0'})
        #self.fields['pointmake'].widget.attrs.update({'class': 'sub-category', 'data-category': '1'})
        #self.fields['basemake'].widget.attrs.update({'class': 'sub-category', 'data-category': '2'})


class ChangeEmailForm(forms.Form):
    current_email = forms.EmailField(
        label='現在のメールアドレス',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '現在のメールアドレス'}),
    )
    new_email = forms.EmailField(
        label='新しいメールアドレス',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '新しいメールアドレス'}),
    )
    confirm_email = forms.EmailField(
        label='メールアドレス再入力',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'メールアドレス再入力'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        new_email = cleaned_data.get("new_email")
        confirm_email = cleaned_data.get("confirm_email")
        if new_email != confirm_email:
            raise forms.ValidationError("新しいメールアドレスが一致しません。")
        return cleaned_data

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','age', 'gender', 'skin_type', 'personal_color', 'profile_image']

    def clean_profile_image(self):
        profile_image = self.cleaned_data.get('profile_image')
        if profile_image:
            # 画像サイズなどのバリデーションを追加できます
            if profile_image.size > 5 * 1024 * 1024:  # 5MB以上の画像を拒否
                raise forms.ValidationError("画像のサイズは5MB以下にしてください。")
        return profile_image
