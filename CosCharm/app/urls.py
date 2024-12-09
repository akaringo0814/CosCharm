from django.urls import path
from . import views


urlpatterns = [
    path('settings/', views.settings, name='settings'),
    path('email_change/', views.email_change, name='email_change'),
    path('password_change/', views.password_change, name='password_change'),
    #path('my-cosmetics/', views.my_cosme, name='my_cosmetics'),
    path('my_cosmetics/', views.my_cosmetics, name='my_cosmetics'),
    path('faovrites-cosme/', views.favorites_cosme, name='favorites_cosme'),
    path('my_cosme-favorites', views.favorites_cosme, name='my_cosme_favorites'),
    path('my-cosme-detail/', views.my_cosme_detail, name='my_cosme_detail'),
    #path('my-cosmetics-register/', views.my_cosmetic_register, name='my_cosmetics_register'),
    path('my_cosmetic_register/', views.my_cosmetic_register, name='my_cosmetic_register'),
    path('my-make-post/', views.my_make_post, name='my_make_post'),
    path('my-make-detail/', views.my_make_detail, name='my_make_detail'),
    path('favorites-make/', views.my_make_detail, name='favorites_make'),
    path('my_page/', views.my_page, name='my_page'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('user-page/', views.user_page, name='user_page'),
    #path('my-page/', views.user_page, name='my_page'),
    path('liked-posts/', views.liked_posts, name='liked_posts'),
    path('follower_list/', views.follower_list, name='follower_list'),
    path('following_list/', views.following_list, name='following_list'),
    path('logout/', views.logout, name='logout'),
    path('update_profile/', views.update_profile, name='update_profile'),


]
