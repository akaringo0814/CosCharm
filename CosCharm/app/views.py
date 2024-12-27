from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignupForm, LoginForm
from .models import MyMake, MyCosmetic, CosmeticMaster, Follow, User
from .forms import ChangeEmailForm, ProfileForm, CosmeticForm
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.conf import settings
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
import os
from django import forms
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404, redirect , Http404
from django.core.paginator import Paginator
import json



class PortfolioView(View):
    def get(self, request):
        return render(request, "portfolio.html")

class SignupView(View): 
    def get(self,request):
        return render(request, "signup.html")
        form = SignupForm()
        return render(request, "signup.html", context={
            "form":form
        })
    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        return render(request, "signup.html", context={
            "form": form 
        })


class LoginView(View): 
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect("home")
        return render(request, "login.html", {"form": form})


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"
    login_url = "login"

    def get(self, request):
        # フォローしているユーザーを取得
        followed_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
        
        # フォローしているユーザーの投稿を取得
        follow_user_posts = MyMake.objects.filter(
            user__in=followed_users
        ).order_by("-created_at")
        
        # 未使用のコスメを取得
        unused_cosmetics = MyCosmetic.objects.filter(
            user=request.user, used_in_make=False
        )
        
        # フォローしているユーザーオブジェクトを取得
        users_followed = User.objects.filter(id__in=followed_users)
        
        context = {
            'follow_user_posts': follow_user_posts,
            'unused_cosmetics': unused_cosmetics,
            'users_followed': users_followed
        }
        return render(request, 'home.html', context)

def logout(request):
    auth_logout(request)
    return redirect('/login/')



def my_cosmetics(request):
    cosmetics = CosmeticMaster.objects.all()
    return render(request, 'my_cosmetics.html', {'cosmetics': cosmetics})

#def my_cosmetic_register(request):
    if request.method == 'POST':
        cosmetic_id = request.POST.get('cosmetic_id')
        is_favorite = request.POST.get('is_favorite') == 'on'
        usage_status = request.POST.get('usage_status')

        cosmetic = CosmeticMaster.objects.get(id=cosmetic_id)
        cosmetic.is_favorite = is_favorite
        cosmetic.usage_status = usage_status
        cosmetic.save()

        return redirect('my_cosmetics')
    
    cosmetics = CosmeticMaster.objects.all()
    return render(request, 'my_cosmetic_register.html', {'cosmetics': cosmetics})

#def my_cosmetic_detail(request):
    return render(request, 'my_cosmetic_detail.html') #マイコスメお気に入り


def load_cosmetic_data():
    # 正しいパスを指定して cosmetic.json を読み込み
    json_path = os.path.join(settings.BASE_DIR, 'app', 'fixtures', 'cosmetic.json')
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"cosmetic.json file not found at {json_path}")

    with open(json_path, 'r', encoding='utf-8') as f:
        cosmetics = json.load(f)
    return cosmetics

# グローバル変数としてコスメデータをロード
COSMETIC_DATA = load_cosmetic_data()

# その他のビュー関数やクラス










#def my_cosmetic_detail(request, pk):
    # 正しいパスを指定して cosmetic.json を読み込み
    #json_path = os.path.join(settings.BASE_DIR, 'app', 'fixtures', 'cosmetic.json')
    #if not os.path.exists(json_path):
        #raise Http404("cosmetic.json file not found")

    #with open(json_path, 'r', encoding='utf-8') as f:
        #cosmetics = json.load(f)

    # pk に基づいてコスメティックを検索
    #cosmetic = next((item for item in cosmetics if item["id"] == pk), None)
    
    #if not cosmetic:
        #raise Http404("Cosmetic not found")

   # return render(request, 'my_cosmetic_detail.html', {'cosmetic': cosmetic})


def delete_my_cosmetic(request, pk):
    cosmetic = get_object_or_404(CosmeticMaster, pk=pk)
    cosmetic.delete()
    return redirect('my_cosmetic')  # マイコスメ一覧画面のURLにリダイレクト


def my_cosmetic_detail(request, pk):
    print(f"Fetching MyCosmetic with pk={pk}")
    cosmetic = get_object_or_404(CosmeticMaster, pk=pk)
    print(f"Found MyCosmetic: {cosmetic}")
    return render(request, 'my_cosmetic_detail.html', {'cosmetic': cosmetic})

#def my_cosmetic_detail(request, pk):
    cosmetic = get_object_or_404(MyCosmetic, pk=pk)
    return render(request, 'my_cosmetic_detail.html', {'cosmetic': cosmetic})

def delete_my_cosmetic(request, pk):
    cosmetic = get_object_or_404(MyCosmetic, pk=pk)
    cosmetic.delete()
    return redirect('my_cosmetic')  # マイコスメ一覧画面のURLにリダイレクト

def favorites_cosme(request):
    # お気に入りのコスメをフィルタリング
    favorite_cosmetics_list = MyCosmetic.objects.filter(is_favorite=True)

    # ページネーションの設定
    paginator = Paginator(favorite_cosmetics_list, 10)  # 1ページあたり10件表示
    page_number = request.GET.get('page')
    favorite_cosmetics = paginator.get_page(page_number)
    
    return render(request, 'favorites_cosme.html', {'favorite_cosmetics': favorite_cosmetics})


#def my_cosmetic_register(request):
    return render(request, 'my_cosme_register.html') #マイコスメ登録画面

#def my_cosmetic_register(request):
    if request.method == 'POST':
        form = CosmeticForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('my_cosme')  # 登録後に一覧ページに移動
    else:
        form = CosmeticForm()
    return render(request, 'my_cosmetic_register.html', {'form': form})



#def search_cosmetics(request):
    keyword = request.GET.get('keyword', '')
    category = request.GET.get('category', '')

    # 検索ロジック
    cosmetics = CosmeticMaster.objects.all()
    if keyword:
        cosmetics = cosmetics.filter(cosmetic_name__icontains=keyword)
    if category:
        cosmetics = cosmetics.filter(subcategory=category)

    # JSON 形式で返す
    results = list(cosmetics.values('id', 'cosmetic_name', 'category', 'subcategory'))
    return JsonResponse({'results': results})

# コスメの検索
def search_cosmetics(request):
    keyword = request.GET.get('keyword', '').lower()
    results = []
    # 簡易的な検索ロジック（カテゴリ内検索）
    for category, items in COSMETIC_CATEGORIES.items():
        filtered_items = [item for item in items if keyword in item.lower()]
        if filtered_items:
            results.append({"category": category, "items": filtered_items})
    return JsonResponse({"results": results})

def my_make_post(request):
    return render(request, 'my_make_post.html') #マイメイク投稿画面


# 初期データ
COSMETIC_CATEGORIES = {
    "フェイスケア": ["化粧水", "乳液", "美容液"],
    "ポイントメイク": ["アイブロウ", "アイシャドウ", "リップ"],
    "ベースメイク": ["下地", "ファンデーション", "フェイスパウダー"],
}

#コスメの登録画面表示
def my_cosmetic_register(request):
    context = {
        "categories": COSMETIC_CATEGORIES,
        "cosmetics": CosmeticMaster.objects.all(),
    }
    if request.method == 'POST':
        # POSTデータからコスメ情報を取得
        cosmetic_id = request.POST.get('cosmetic_id')
        is_favorite = 'is_favorite' in request.POST
        usage_status = request.POST.get('usage_status')
        if cosmetic_id:
            cosmetic = CosmeticMaster.objects.get(id=cosmetic_id)
            # コスメ登録処理
            MyCosmetic.objects.create(
                user=request.user,
                cosmetic=cosmetic,
                is_favorite=is_favorite,
                usage_status=usage_status
            )
            
            return redirect('my_cosmetics')
        else:
            # cosmetic_id が None の場合のエラーメッセージを追加
            context['error'] = "コスメを選択してください。"
    return render(request, 'my_cosmetic_register.html', context)


# カテゴリに基づくコスメの検索
def search_cosmetics(request):
    category = request.GET.get('category', '').lower()
    results = []

    if category:
        cosmetics = CosmeticMaster.objects.filter(category__iexact=category)
        results = [{'id': cosmetic.id, 'name': cosmetic.name} for cosmetic in cosmetics]

    return JsonResponse({"results": results})

# 初期コスメデータの取得
def get_initial_cosmetics(request):
    # cosmetic.jsonファイルのパス
    file_path = os.path.join(settings.BASE_DIR, 'static/data/cosmetic.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        cosmetics = json.load(f)

    # 必要なデータだけ抽出（fieldsのみ）
    filtered_cosmetics = [
        {
            "name": item["fields"]["name"],
            "brand": item["fields"]["brand"],
            "category": item["fields"]["category"],
            "price": item["fields"]["price"]
        }
        for item in cosmetics
    ]

    return JsonResponse({"cosmetics": filtered_cosmetics})


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


