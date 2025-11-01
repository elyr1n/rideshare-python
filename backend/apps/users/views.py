from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
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
            messages.success(request, "Аккаунт успешно создан!")
            return redirect("scooters:scooter-models-list")

        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
        except Exception as e:
            messages.error(request, f"Ошибка при создании аккаунта: {str(e)}")

    return render(request, "users/register.html")


@login_required()
def profile_view(request):
    return render(request, "users/profile.html")


@login_required
def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password1 = request.POST.get("password1")
        new_password2 = request.POST.get("password2")

        user = request.user

        if not user.check_password(old_password):
            messages.error(request, "Старый пароль неверен")
            return redirect("users:change_password")

        if new_password1 != new_password2:
            messages.error(request, "Новые пароли не совпадают")
            return redirect("users:change_password")

        if len(new_password1) < 8:
            messages.error(request, "Пароль должен содержать минимум 8 символов")
            return redirect("users:change_password")

        user.set_password(new_password1)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Пароль успешно изменён")
        return redirect("users:profile")

    return render(request, "users/change_password.html")
