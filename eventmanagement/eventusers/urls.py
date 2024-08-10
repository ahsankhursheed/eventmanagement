from django.urls import include
from django.urls import path
from .import views

app_name = "users"

urlpatterns = [
    path("signup/", views.user_signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("", views.success, name="success"),

]