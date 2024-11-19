from django.shortcuts import render, redirect 
from django.views import View
from app.forms import Signupform 
from django.contrib.auth import login

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

class HomeView(View): 
    def get(self,request):
        return render(request, "home.html")      