
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import CustomSignUpForm


def signup_view(request):
    if request.method == "POST":
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to TaskHero, {user.first_name}!")
            return redirect("taskhero:home")
    else:
        form = CustomSignUpForm()
    return render(request, "account/sign-up.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("taskhero:all_task")
    else:
        form = AuthenticationForm()
    return render(request, "account/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect('taskhero:home')