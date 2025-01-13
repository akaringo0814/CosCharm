from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q, Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, TemplateView
import json
import logging
import os
from django.contrib import messages  

from .forms import (
    SignupForm, LoginForm, MyMakeForm, ChangeEmailForm,
    ProfileForm, CosmeticForm, MyCosmeticForm, MyCosmeticEditForm
)
from .models import MyMake, MyCosmetic, CosmeticMaster, Follow, User, MyMakeCosmetic, Favorite




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


class CustomLoginView(LoginView):
    template_name = 'login.html'  # カスタムテンプレートのパス


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"
    login_url = "login"

    def get(self, request):
        # フォローしているユーザーを取得
        followed_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)

        # フィルタを取得
        personal_color = request.GET.get('personal_color')
        skin_type = request.GET.get('skin_type')

        # フォローしているユーザーの投稿を取得
        follow_user_posts = MyMake.objects.filter(
            user__in=followed_users
        ).order_by("-created_at")

        if personal_color:
            follow_user_posts = follow_user_posts.filter(user__personal_color=personal_color)
        
        if skin_type:
            follow_user_posts = follow_user_posts.filter(user__skin_type=skin_type)

        # 未使用のコスメを取得（使用状況が「未使用」のコスメ）
        unused_cosmetics_qs = MyCosmetic.objects.filter(
            user=request.user, usage_status='not_used'
        )

        # 手動で重複を排除
        cosmetics_seen = set()
        unused_cosmetics = []
        for cosmetic in unused_cosmetics_qs:
            if cosmetic.cosmetic.cosmetic_name not in cosmetics_seen:
                unused_cosmetics.append(cosmetic)
                cosmetics_seen.add(cosmetic.cosmetic.cosmetic_name)

        # フォローしているユーザーオブジェクトを取得
        users_followed = User.objects.filter(id__in=followed_users)

        context = {
            'follow_user_posts': follow_user_posts,
            'unused_cosmetics': unused_cosmetics,
            'users_followed': users_followed,
            'personal_color': personal_color,  # コンテキストに追加
            'skin_type': skin_type  # コンテキストに追加
        }
        return render(request, self.template_name, context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('/login/')

@login_required
def my_cosmetics(request):
    query = request.GET.get('q')
    include_used = request.GET.get('include_used') == 'on'

    # データが存在するもののみフィルタリング
    latest_cosmetic_ids = MyCosmetic.objects.filter(user=request.user, cosmetic__isnull=False).values('cosmetic').annotate(latest_id=Max('id')).values('latest_id')
    cosmetics = MyCosmetic.objects.filter(id__in=latest_cosmetic_ids)

    if query:
        cosmetics = cosmetics.filter(
            Q(cosmetic__cosmetic_name__icontains=query) |
            Q(cosmetic__brand__icontains=query)
        )

    if not include_used:
        cosmetics = cosmetics.filter(Q(usage_status='not_used') | Q(usage_status='in_use'))
    
    return render(request, 'my_cosmetics.html', {'cosmetics': cosmetics, 'query': query, 'include_used': include_used})


@login_required
def my_cosmetic_register(request):
    query = request.GET.get('q', '')
    cosmetics = CosmeticMaster.objects.all()
    
    if query:
        cosmetics = cosmetics.filter(cosmetic_name__icontains=query)
    
    if request.method == 'POST':
        cosmetic_id = request.POST.get('cosmetic_id')
        is_favorite = request.POST.get('is_favorite') == 'on'
        usage_status = request.POST.get('usage_status')

        cosmetic = CosmeticMaster.objects.get(id=cosmetic_id)
        cosmetic.is_favorite = is_favorite
        cosmetic.usage_status = usage_status
        cosmetic.save()

        return redirect('my_cosmetics')
    
    context = {
        'cosmetics': cosmetics,
        'filtered_cosmetics': cosmetics,  # フィルタリングされたコスメをテンプレートに渡す
        'query': query
    }
    
    return render(request, 'my_cosmetic_register.html', context)




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




@login_required
def my_cosmetic_detail(request, pk):
    cosmetic_master = get_object_or_404(CosmeticMaster, pk=pk)
    my_cosmetic = MyCosmetic.objects.filter(cosmetic=cosmetic_master, user=request.user).order_by('-updated_at').first()

    # フォロワーのユーザーを取得
    followers = Follow.objects.filter(following=request.user).values_list('follower', flat=True)

    # 自分とフォロワーのメイクを取得
    my_make_cosmetics = MyMakeCosmetic.objects.filter(cosmetic=cosmetic_master, my_make__user__in=[request.user] + list(followers))

    # メインコスメ及び他使用コスメのメイクIDを取得
    main_cosmetics = my_make_cosmetics.filter(is_main=True).values_list('my_make', flat=True)
    other_cosmetics = my_make_cosmetics.filter(is_main=False).values_list('my_make', flat=True)

    # 自分とフォロワーのすべての関連メイクを取得
    all_related_makes = MyMake.objects.filter(id__in=set(list(main_cosmetics) + list(other_cosmetics)))

    context = {
        'cosmetic_master': cosmetic_master,
        'my_cosmetic': my_cosmetic,
        'my_make_using_cosmetic': all_related_makes,
    }
    return render(request, 'my_cosmetic_detail.html', context)


@login_required
def delete_my_cosmetic(request, pk):
    my_cosmetic = get_object_or_404(MyCosmetic, pk=pk, user=request.user)
    my_cosmetic.delete()
    return redirect('my_cosmetics')

@login_required
def favorites_cosme(request):
    # 削除されていないレコードを対象とする
    filtered_cosmetics = MyCosmetic.objects.filter(user=request.user, is_deleted=False)

    # cosmetic_id ごとに最新の updated_at を持つレコードを取得
    latest_cosmetics = (
        filtered_cosmetics
        .values('cosmetic_id')
        .annotate(latest_id=Max('id'))  # 最新の ID を取得
    )

    # 最新のレコードで is_favorite=True のものをフィルタリング
    favorite_cosmetics_list = MyCosmetic.objects.filter(
        id__in=[item['latest_id'] for item in latest_cosmetics],
        is_favorite=True
    ).order_by('-updated_at')

    # デバッグ用にログを出力
    print(favorite_cosmetics_list.query)  # 実行されるSQL
    print(list(favorite_cosmetics_list))  # 取得結果を確認

    # ページネーションの設定
    paginator = Paginator(favorite_cosmetics_list, 10)  # 1ページあたり10件表示
    page_number = request.GET.get('page')
    favorite_cosmetics = paginator.get_page(page_number)
    
    return render(request, 'favorites_cosme.html', {'favorite_cosmetics': favorite_cosmetics})



# 初期データ
COSMETIC_CATEGORIES = {
    "フェイスケア": ["化粧水", "乳液", "美容液"],
    "ポイントメイク": ["アイブロウ", "アイシャドウ", "リップ"],
    "ベースメイク": ["下地", "ファンデーション", "フェイスパウダー"],
}

@login_required
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



@login_required
def search_cosmetics(request):
    keyword = request.GET.get('keyword', '').lower()
    category = request.GET.get('category', '').lower()

    query = CosmeticMaster.objects.all()

    if keyword:
        query = query.filter(name__icontains=keyword)
    if category:
        query = query.filter(category__icontains=category)

    results = [{'id': cosmetic.id, 'name': cosmetic.name} for cosmetic in query]

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

@login_required
def my_cosmetic_edit(request, pk):
    my_cosmetic = get_object_or_404(MyCosmetic, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MyCosmeticEditForm(request.POST, instance=my_cosmetic)
        if form.is_valid():
            form.save()
            return redirect('my_cosmetics')
    else:
        form = MyCosmeticEditForm(instance=my_cosmetic)
    return render(request, 'my_cosmetic_edit.html', {'form': form, 'my_cosmetic': my_cosmetic})

@login_required
def my_cosmetic_delete(request, pk):
    my_cosmetic = get_object_or_404(MyCosmetic, pk=pk, user=request.user)
    if request.method == 'POST':
        my_cosmetic.delete()
        return redirect('my_cosmetics')
    return render(request, 'my_cosmetic_confirm_delete.html', {'my_cosmetic': my_cosmetic})


@login_required
def my_make_detail(request, pk):
    my_make = get_object_or_404(MyMake, pk=pk)
    main_cosmetic = MyMakeCosmetic.objects.filter(my_make=my_make, is_main=True).first()
    other_cosmetics = MyMakeCosmetic.objects.filter(my_make=my_make, is_main=False)
    other_cosmetic_ids = other_cosmetics.values_list('cosmetic__pk', flat=True)
    all_cosmetics = CosmeticMaster.objects.all()
    is_favorite = Favorite.objects.filter(user=request.user, my_make=my_make).exists()
    return render(request, 'my_make_detail.html', {
        'my_make': my_make,
        'main_cosmetic': main_cosmetic.cosmetic.cosmetic_name if main_cosmetic else None,
        'other_cosmetics': other_cosmetics,
        'other_cosmetic_ids': other_cosmetic_ids,
        'all_cosmetics': all_cosmetics,
        'is_favorite': is_favorite,
    })

@login_required
def update_main_cosmetic(request, pk):
    my_make = get_object_or_404(MyMake, pk=pk)
    cosmetic_id = request.POST.get("main_cosmetic")
    if cosmetic_id:
        # 既存のメインコスメをリセット
        my_make.cosmetics.filter(is_main=True).delete()
        # 新しいメインコスメを登録
        cosmetic = get_object_or_404(CosmeticMaster, pk=cosmetic_id)
        MyMakeCosmetic.objects.create(my_make=my_make, cosmetic=cosmetic, is_main=True)
    return redirect('my_make_detail', pk=pk)

@login_required
def update_other_cosmetics(request, pk):
    my_make = get_object_or_404(MyMake, pk=pk)
    cosmetic_ids = request.POST.getlist("other_cosmetics")
    if cosmetic_ids:
        # 他使用コスメをリセット
        my_make.cosmetics.filter(is_main=False).delete()
        # 新しい他使用コスメを登録
        cosmetics = CosmeticMaster.objects.filter(pk__in=cosmetic_ids)
        for cosmetic in cosmetics:
            MyMakeCosmetic.objects.create(my_make=my_make, cosmetic=cosmetic, is_main=False)
    return redirect('my_make_detail', pk=pk)

@login_required
def delete_my_make(request, pk):
    my_make = get_object_or_404(MyMake, pk=pk)
    if request.method == "POST":
        my_make.delete()
        return redirect('home')  # 削除後のリダイレクト先を設定
    return render(request, 'delete_confirmation.html', {'my_make': my_make})




@login_required
def my_make_post_new(request):
    all_cosmetics = CosmeticMaster.objects.all()
    if request.method == 'POST':
        form = MyMakeForm(request.POST, request.FILES)
        if form.is_valid():
            my_make = form.save(commit=False)
            my_make.user = request.user
            my_make.save()
            form.save_m2m()
            other_cosmetics = form.cleaned_data.get('other_cosmetics', [])
            main_cosmetic = form.cleaned_data.get('main_cosmetic')

            for cosmetic in other_cosmetics:
                MyMakeCosmetic.objects.create(my_make=my_make, cosmetic=cosmetic, is_main=False)

            if main_cosmetic:
                MyMakeCosmetic.objects.create(my_make=my_make, cosmetic=main_cosmetic, is_main=True)
            
            return redirect('my_make_detail', pk=my_make.pk)
    else:
        form = MyMakeForm()
    return render(request, 'my_make_post.html', {'form': form, 'all_cosmetics': all_cosmetics, 'main_cosmetic_id': None, 'other_cosmetic_ids': []})


@login_required
def my_make_post(request, pk):
    my_make = get_object_or_404(MyMake, pk=pk)
    all_cosmetics = CosmeticMaster.objects.all()
    main_cosmetic = MyMakeCosmetic.objects.filter(my_make=my_make, is_main=True).first()
    other_cosmetics = MyMakeCosmetic.objects.filter(my_make=my_make, is_main=False)
    if request.method == 'POST':
        form = MyMakeForm(request.POST, request.FILES, instance=my_make)
        if form.is_valid():
            form.save()
            MyMakeCosmetic.objects.filter(my_make=my_make).delete()
            other_cosmetics = form.cleaned_data.get('other_cosmetics', [])
            main_cosmetic = form.cleaned_data.get('main_cosmetic')

            for cosmetic in other_cosmetics:
                MyMakeCosmetic.objects.create(my_make=my_make, cosmetic=cosmetic, is_main=False)

            if main_cosmetic:
                MyMakeCosmetic.objects.create(my_make=my_make, cosmetic=main_cosmetic, is_main=True)
            
            return redirect('my_make_detail', pk=my_make.pk)
    else:
        form = MyMakeForm(instance=my_make)
    main_cosmetic_id = main_cosmetic.cosmetic.pk if main_cosmetic else None
    other_cosmetic_ids = other_cosmetics.values_list('cosmetic__pk', flat=True)
    return render(request, 'my_make_post.html', {'form': form, 'all_cosmetics': all_cosmetics, 'main_cosmetic_id': main_cosmetic_id, 'other_cosmetic_ids': other_cosmetic_ids})

@login_required
def modal_select_cosmetics(request):
    # 必要に応じてデータをテンプレートに渡す
    return render(request, 'modal_select_cosmetics.html')


@login_required
def favorites_make(request):
    favorites_list = Favorite.objects.filter(user=request.user).select_related('my_make')
    paginator = Paginator(favorites_list, 10)  # 1ページに表示するアイテム数を設定
    page_number = request.GET.get('page')
    favorites = paginator.get_page(page_number)
    return render(request, 'favorites_make.html', {'favorites': favorites})

@login_required
def toggle_favorite(request, pk):
    my_make = get_object_or_404(MyMake, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, my_make=my_make)
    if not created:
        favorite.delete()
    return redirect('my_make_detail', pk=my_make.pk)



@login_required
def my_page(request):
    profile = get_object_or_404(User, username=request.user.username)
    followers = Follow.objects.filter(following=request.user)
    following = Follow.objects.filter(follower=request.user)

    # 自分の投稿を取得
    my_posts = MyMake.objects.filter(user=request.user).order_by("-created_at")

    return render(request, 'my_page.html', {
        'profile': profile,
        'followers': followers.count(),
        'following': following.count(),
        'my_posts': my_posts,  # 自分の投稿をコンテキストに追加
    })

@login_required
def user_page(request):
    return render(request, 'user_page.html')


#プロフィール編集画面
@login_required
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



@login_required
def email_change(request):
    if request.method == 'POST':
        form = ChangeEmailForm(user=request.user, data=request.POST)
        if form.is_valid():
            # メールアドレスの更新処理
            request.user.email = form.cleaned_data['new_email']
            request.user.save()
            # 成功メッセージを追加してリダイレクト
            messages.success(request, 'メールアドレスが更新されました。')
            return redirect('my_page')  # プロフィールページなどの適切なリダイレクト先に変更してください
    else:
        form = ChangeEmailForm(user=request.user)
    
    return render(request, 'email_change.html', {'form': form})



@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # パスワード変更後もログイン状態を保持
            messages.success(request, 'パスワードが更新されました。')
            return redirect('home')  # ホーム画面にリダイレクト
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'password_change.html', {'form': form})


@login_required
def liked_posts(request):
    return render(request, 'liked_posts.html')

@login_required
def favorites_make(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('my_make')
    return render(request, 'favorites_make.html', {'favorites': favorites})

# フォロー一覧
@login_required
def following_list(request):
    followings = Follow.objects.filter(follower=request.user)
    return render(request, 'following_list.html', {'followings': followings})

# フォロワー一覧
@login_required
def follower_list(request):
    followers = Follow.objects.filter(following=request.user)
    return render(request, 'follower_list.html', {'followers': followers})

@login_required
def settings(request):
    # 設定ページの処理
    return render(request, 'settings_template.html')

@login_required
def update_profile(request):
    # プロフィール更新のロジック
    return render(request, 'update_profile.html')


# 他ユーザーのユーザーページ
@login_required
def user_page(request, user_id):
    user_profile = get_object_or_404(User, id=user_id)
    my_make_list = MyMake.objects.filter(user=user_profile).order_by('-created_at')
    is_following = Follow.objects.filter(follower=request.user, following=user_profile).exists()

    context = {
        'user_profile': user_profile,
        'my_make_list': my_make_list,
        'is_following': is_following,
    }
    return render(request, 'user_page.html', context)

# フォロワー一覧
@login_required
def follower_list(request, user_id):
    user_profile = get_object_or_404(User, id=user_id)
    followers = Follow.objects.filter(following=user_profile).select_related('follower')
    context = {
        'user_profile': user_profile,
        'followers': [f.follower for f in followers],
    }
    return render(request, 'follower_list.html', context)

# フォロー中のユーザー一覧
@login_required
def following_list(request, user_id):
    user_profile = get_object_or_404(User, id=user_id)
    following = Follow.objects.filter(follower=user_profile).select_related('following')
    context = {
        'user_profile': user_profile,
        'following': [f.following for f in following],
    }
    return render(request, 'following_list.html', context)

# フォロー処理
@login_required
def follow(request, user_id):
    following = get_object_or_404(User, id=user_id)
    Follow.objects.get_or_create(follower=request.user, following=following)
    return redirect('user_page', user_id=user_id)

#フォロー解除処理
@login_required
def unfollow(request, user_id):
    following = get_object_or_404(User, id=user_id)
    Follow.objects.filter(follower=request.user, following=following).delete()
    return redirect('user_page', user_id=user_id)


@login_required
def follow_user_posts(request):
    personal_color = request.GET.get('personal_color')
    follow_user_posts = MyMake.objects.filter(user__in=request.user.following.all())

    if personal_color:
        follow_user_posts = follow_user_posts.filter(user__personal_color=personal_color)

    return render(request, 'timeline.html', {'follow_user_posts': follow_user_posts, 'personal_color': personal_color})


logger = logging.getLogger(__name__)

@login_required
def follow_user(request, user_id):
    if request.method == "POST":
        target_user = get_object_or_404(User, id=user_id)
        request.user.following.add(target_user)
        return JsonResponse({"status": "followed"})
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def unfollow_user(request, user_id):
    if request.method == "POST":
        target_user = get_object_or_404(User, id=user_id)
        request.user.following.remove(target_user)
        return JsonResponse({"status": "unfollowed"})
    return JsonResponse({"error": "Invalid request"}, status=400)
