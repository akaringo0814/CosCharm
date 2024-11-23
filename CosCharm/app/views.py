from django.shortcuts import render, redirect 
from django.views import View
from app.forms import Signupform, LoginForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MyMake, MyCosme  # 投稿やコスメデータを管理するモデル

# Create your views here.

class PortfolioView(View): 
    def get(self,request):
        return render(request, "portfolio.html")
    
class SignupView(View): 
    def get(self,request):
        form = Signupform()
        return render(request, "signup.html", context={
            "form":form
        })
    def post(self, request):
        form = Signupform(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        return render(request, "signup.html", context={
            "form": form 
        })
    
class LoginView(View): 
    def get(self,request):
        return render(request, "login.html")  
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            #user = form.save()
            login(request, form.user)
            return redirect("home")
        return render(request, "login.html", context={
            "form": form 
        })

class HomeView(View,LoginRequiredMixin): 
    login_url = "login"
    def get(self,request):
        return render(request, "home.html")      


def home(request):
    # 右側：フォローユーザーの投稿を取得（日時順）
    follow_user_posts = MyMake.objects.filter(user__in=request.user.following.all()).order_by('-created_at')
    
    # 左側：未使用の所持コスメを取得
    unused_cosmetics = MyCosme.objects.filter(user=request.user, used_in_make=False)
    
    return render(request, 'home.html', {
        'follow_user_posts': follow_user_posts,
        'unused_cosmetics': unused_cosmetics
    })
def settings(request): 
    # ここに処理を記述 
    return render(request, 'settings.html')

def my_cosme(request):
    return render(request, 'my_cosme.html')

def my_cosme_detail(request):
    return render(request, 'my_cosme_detail.html') #マイコスメお気に入り

def favorites_cosme(request): 
    # ここに処理を記述 
    return render(request, 'favorites_cosme.html')

def my_cosme_register(request):
    return render(request, 'my_cosme_register.html') #マイコスメ登録画面

def my_make_post(request):
    return render(request, 'my_make_post.html') #マイメイク投稿画面

def my_make_detail(request):
    return render(request, 'my_make_detail.html') #マイメイク詳細画面

def favorites_make(request):
    return render(request, 'favorites_make.html') #マイメイクお気に入り

def my_page(request):
    return render(request, 'my_page.html')

def user_page(request):
    return render(request, 'user_page.html')

def profile_edit(request):
    return render(request, 'profile_edit.html')


def email_change(request):
    return render(request, 'email_change.html')

def password_change(request):
    return render(request, 'password_change.html')

def liked_posts(request):
    return render(request, 'liked_posts.html')

def follower_list(request):
    return render(request, 'follower_list.html')

def following_list(request):
    return render(request, 'following_list_list.html')

def logout_view(request):
    # ログアウト処理を追加
    return render(request, 'logout.html')

