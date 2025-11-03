from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("profile/<int:user_id>/", views.profile_view, name="user_profile"),
    path("change-password/", views.change_password, name="change_password"),
    path("password-reset-sent/", views.password_reset_sent, name="password_reset_sent"),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        views.password_reset_confirm,
        name="password_reset_confirm",
    ),
]
