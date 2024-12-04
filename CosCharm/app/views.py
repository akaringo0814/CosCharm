from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import Signupform, LoginForm
from .models import MyMake, MyCosmetic
from .forms import ChangeEmailForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, get_object_or_404
from .models import  Follow, User
from .forms import ProfileForm

class PortfolioView(View):
    def get(self, request):
        return render(request, "portfolio.html")

class SignupView(View):
    def get(self, request):
        form = Signupform()
        return render(request, "signup.html", {"form": form})

    def post(self, request):
        form = Signupform(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        return render(request, "signup.html", {"form": form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST, request=request)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.POST.get("next") or "home"  # 'next'パラメータの確認
            return redirect(next_url)
        return render(request, "login.html", {"form": form})

class HomeView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        follow_user_posts = MyMake.objects.filter(
            user__in=request.user.following.all()
        ).order_by("-created_at")
        unused_cosmetics = MyCosmetic.objects.filter(
            user=request.user, used_in_make=False
        )
        return render(request, "home.html", {
            "follow_user_posts": follow_user_posts,
            "unused_cosmetics": unused_cosmetics,
        })
    def get(self, request):
        # フォローしているユーザーのIDリストを取得
        followed_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
        
        # フォローされているユーザーを取得
        users_followed = User.objects.filter(id__in=followed_users)
        
        context = {
            'users_followed': users_followed
        }
        return render(request, 'home.html', context)
#@login_required
#def logout(request):
    #logout(request)
    #return redirect('login')

def logout(request):
    auth_logout(request)
    return redirect('/login/') 



#@login_required
#def my_cosmetics(request):
    #my_cosmetics = MyCosmetic.objects.filter(user=request.user)
    #return render(request, "my_cosmetics.html", {"my_cosmetics": my_cosmetics})

def my_cosme(request):
    my_cosmetics = MyCosmetic.objects.filter(user=request.user)
    return render(request, "my_cosmetics.html")#, {"my_cosmetics": my_cosmetics})
    # ビューのロジック
    #return render(request, 'my_cosmetics.html')#上と一緒？不必要？

#def logout(request):
    auth_logout(request)
    return redirect(request,"login.html")


def my_cosme_detail(request):
    return render(request, 'my_cosme_detail.html') #マイコスメお気に入り

def favorites_cosme(request): 
    # ここに処理を記述 
    return render(request, 'favorites_cosme.html') #favorite_cosme my_cosme_favotiteどちらか

def my_cosme_favorites(request):
    # ここに処理を記述
    return render(request, 'my_cosme_favorites.html')

def my_cosmetic_register(request):
    return render(request, 'my_cosme_register.html') #マイコスメ登録画面

def my_make_post(request):
    return render(request, 'my_make_post.html') #マイメイク投稿画面

def my_make_detail(request):
    return render(request, 'my_make_detail.html') #マイメイク詳細画面

def favorites_make(request):
    return render(request, 'favorites_make.html') #マイメイクお気に入り

#マイページ
def my_page(request):
    profile = get_object_or_404(User, username=request.user.username)
    followers = Follow.objects.filter(following=request.user)
    following = Follow.objects.filter(follower=request.user)
    return render(request, 'my_page.html', {
        'profile': profile,
        'followers': followers.count(),
        'following': following.count()
    })


def user_page(request):
    return render(request, 'user_page.html')


#プロフィール編集画面
def profile_edit(request):
    profile = get_object_or_404(User, username=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('my_page')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile_edit.html', {'form': form})



def email_change(request):
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            # フォームのデータを取得
            current_email = form.cleaned_data['current_email']
            new_email = form.cleaned_data['new_email']

            # メールアドレス変更処理をここに記述
            print(f"Current Email: {current_email}, New Email: {new_email}")

            # 成功後にホーム画面へリダイレクト
            return redirect('home')  # 'home' はホーム画面のURL名
    else:
        form = ChangeEmailForm()

    return render(request, 'email_change.html', {'form': form})



@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # パスワード変更後もログイン状態を保持
            return redirect('home')  # ホーム画面にリダイレクト
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'password_change.html', {'form': form})


def liked_posts(request):
    return render(request, 'liked_posts.html')

def follower_list(request):
    return render(request, 'follower_list.html')

def following_list(request):
    return render(request, 'following_list_list.html')
from django.shortcuts import render
from .models import Follow

# フォロー一覧
def following_list(request):
    followings = Follow.objects.filter(follower=request.user)
    return render(request, 'following_list.html', {'followings': followings})

# フォロワー一覧
def follower_list(request):
    followers = Follow.objects.filter(following=request.user)
    return render(request, 'follower_list.html', {'followers': followers})

def settings(request):
    # 設定ページの処理
    return render(request, 'settings_template.html')

def update_profile(request):
    # プロフィール更新のロジック
    return render(request, 'update_profile.html')


