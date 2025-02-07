from django import forms
from django.contrib.auth.forms import UserCreationForm
from app.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import MyMake, MyCosmetic, CosmeticMaster,MyMakeCosmetic
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm as AuthPasswordChangeForm





class SignupForm(UserCreationForm):
    password1 = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput,
        help_text="8文字以上の英数字を含むパスワードを設定してください。",
    )
    password2 = forms.CharField(
        label="パスワード確認",
        widget=forms.PasswordInput,
        help_text="確認のため、同じパスワードを入力してください。",
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',  # クラス名を追加
            'placeholder': 'メールアドレス'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',  # クラス名を追加
            'placeholder': 'パスワード'
        })
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        self.user = authenticate(email=email, password=password)
        if self.user is None:
            raise forms.ValidationError("認証に失敗しました")
        return self.cleaned_data

# MyMake用フォーム
class MyMakeForm(forms.ModelForm):
    
    class Meta:
        model = MyMake
        fields = ['make_name', 'image']  # 必要なフィールドを指定


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'age', 'gender', 'skin_type', 'personal_color', 'profile_image']

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and age < 0:
            raise forms.ValidationError("年齢は0以上を入力してください。")
        return age

    def clean_profile_image(self):
        profile_image = self.cleaned_data.get('profile_image')
        if profile_image:
            # 画像サイズの制限（例：5MB）
            if profile_image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("画像のサイズは5MB以下にしてください。")
        return profile_image


# MyCosme用フォーム
class MyCosmeticForm(forms.ModelForm):
    cosmetic = forms.ModelChoiceField(
        queryset=CosmeticMaster.objects.all(),
        label="商品名",
        widget=forms.Select
    )

    class Meta:
        model = MyCosmetic
        fields = ['cosmetic', 'used_in_make', 'is_favorite', 'usage_status']


class CosmeticForm(forms.ModelForm):
    class Meta:
        model = CosmeticMaster
        fields = ['cosmetic_name', 'category', 'sub_category', 'photo']
        widgets = {
            'category': forms.Select(),
            'sub_category': forms.TextInput(attrs={'placeholder': 'アイブロウ'}),
            'usage_status': forms.RadioSelect(),  # ラジオボタンで選択
            'favorite': forms.CheckboxInput(),    # チェックボックス
        }


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

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_email(self):
        current_email = self.cleaned_data.get('current_email')
        if current_email != self.user.email:
            raise ValidationError("現在のメールアドレスが一致しません。")
        return current_email

    def clean(self):
        cleaned_data = super().clean()
        new_email = cleaned_data.get("new_email")
        confirm_email = cleaned_data.get("confirm_email")

        if new_email != confirm_email:
            raise ValidationError("新しいメールアドレスが一致しません。")
        return cleaned_data

#class ProfileForm(forms.ModelForm):
    #class Meta:
        model = User
        fields = ['username','age', 'gender', 'skin_type', 'personal_color', 'profile_image']

    #def clean_profile_image(self):
        profile_image = self.cleaned_data.get('profile_image')
        if profile_image:
            # 画像サイズなどのバリデーションを追加できます
            #if profile_image.size > 5 * 1024 * 1024:  # 5MB以上の画像を拒否
                #raise forms.ValidationError("画像のサイズは5MB以下にしてください。")
                pass
        return profile_image
    




class MyMakeForm(forms.ModelForm):
    main_cosmetic = forms.ModelChoiceField(queryset=CosmeticMaster.objects.all(), required=False)
    other_cosmetics = forms.ModelMultipleChoiceField(queryset=CosmeticMaster.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)  # 他使用コスメを複数選択できるようにする

    class Meta:
        model = MyMake
        fields = ['make_name', 'image', 'make_memo', 'main_cosmetic', 'other_cosmetics']

    def save(self, commit=True):
        my_make = super().save(commit=False)
        if commit:
            my_make.save()
            self.save_m2m()
        return my_make


class MyCosmeticForm(forms.ModelForm):
    class Meta:
        model = MyCosmetic
        fields = ['cosmetic', 'is_favorite', 'usage_status']



class MyCosmeticEditForm(forms.ModelForm):
    USAGE_CHOICES = [
        ('not_used', '未使用'),
        ('in_use', '使用中'),
        ('used', '使用済み')
    ]

    usage_status = forms.ChoiceField(
        label='使用状況',
        choices=USAGE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'})
    )

    class Meta:
        model = MyCosmetic
        fields = ['usage_status', 'is_favorite']



class PasswordChangeForm(AuthPasswordChangeForm):
    old_password = forms.CharField(
        label='現在のパスワード',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '現在のパスワード'}),
    )
    new_password1 = forms.CharField(
        label='新しいパスワード',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '新しいパスワード'}),
    )
    new_password2 = forms.CharField(
        label='新しいパスワード（確認）',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '新しいパスワード（確認）'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise ValidationError("現在のパスワードが一致しません。")
        return old_password

