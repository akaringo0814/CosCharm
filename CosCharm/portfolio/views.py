from django.shortcuts import render

def portfolio_index(request):
    """ポートフォリオのトップページを表示"""
    return render(request, 'index.html')
