"""
URL configuration for CosCharm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app.views import PortfolioView, SignupView, LoginView, HomeView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PortfolioView.as_view(), name="portfolio"),
    path('coscharm/signup/', SignupView.as_view(), name="signup"),
    path('coscharm/login/', LoginView.as_view(), name="login"),
    path('coscharm/home/', HomeView.as_view(), name="home"),
    path('', include('portfolio.urls')),  # ポートフォリオをルートに
    path('coscharm/', include('app.urls')),  # アプリを /coscharm/ に
] 
# メディアファイルの公開設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

 
