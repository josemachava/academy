from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm, LoginForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Welcome, {user.first_name}! Your account has been created.")
        return redirect("dashboard")
    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.cleaned_data["user"]
        remember = form.cleaned_data.get("remember_me")
        login(request, user)
        if not remember:
            request.session.set_expiry(0)  # session expires on browser close
        messages.success(request, f"Welcome back, {user.first_name}!")
        return redirect("dashboard")
    return render(request, "login.html", {"form": form})


def logout_view(request):
    messages.info(request, "You've been signed out.")
    logout(request)
    return redirect("login")


@login_required
def dashboard_view(request):
    return render(request, "dashboard.html")
