from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from app.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import MyMake, MyCosmetic, CosmeticMaster,MyMakeCosmetic
#from .models import Profile
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]



class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)  # 非表示にする

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
            #if profile_image.size > 5 * 1024 * 1024:  # 5MB以上の画像を拒否
                #raise forms.ValidationError("画像のサイズは5MB以下にしてください。")
                pass
        return profile_image
    

#class MyMakeForm(forms.ModelForm):
    #class Meta:
        model = MyMake
        fields = ['make_name', 'make_memo', 'image']


#class MyMakeForm(forms.ModelForm):
    #main_cosmetic = forms.ModelChoiceField(queryset=CosmeticMaster.objects.all(), required=False)
    #other_cosmetics = forms.ModelMultipleChoiceField(queryset=CosmeticMaster.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    #class Meta:
        model = MyMake
        fields = ['make_name', 'image', 'make_memo', 'main_cosmetic', 'other_cosmetics']  # フィールドを追加

    #def save(self, commit=True):
        my_make = super().save(commit=False)
        if commit:
            my_make.save()
            self.save_m2m()
        return my_make


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
