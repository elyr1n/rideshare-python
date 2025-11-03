from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from .models import CustomUser


def login_view(request):
    if request.user.is_authenticated:
        return redirect("scooters:scooter-models-list")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "Пожалуйста, заполните все поля.")
            return render(request, "users/login.html")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("scooters:scooter-models-list")
        else:
            messages.error(request, "Неверный email или пароль.")

    return render(request, "users/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из аккаунта.")
    return redirect("users:login")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("scooters:scooter-models-list")

    if request.method == "POST":
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not all([email, first_name, last_name, password1, password2]):
            messages.error(request, "Пожалуйста, заполните все поля.")
            return render(request, "users/register.html")

        if password1 != password2:
            messages.error(request, "Пароли не совпадают.")
            return render(request, "users/register.html")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email уже зарегистрирован.")
            return render(request, "users/register.html")

        try:
            validate_password(password1)

            user = CustomUser.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password1,
            )

            login(request, user)
            return redirect("scooters:scooter-models-list")

        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)

    return render(request, "users/register.html")


@login_required
def profile_view(request, user_id=None):
    profile_user = (
        get_object_or_404(CustomUser, id=user_id) if user_id else request.user
    )
    return render(
        request,
        "users/profile.html",
        {"profile_user": profile_user, "is_own_profile": request.user == profile_user},
    )
