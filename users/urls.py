from django.urls import path
from .views import (
    signup,
    login,
    dashboard,
    logout,
    RegisterClientView,
)


urlpatterns = [
    path("", signup, name="signup"),
    path("login/", login, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("logout/", logout, name="logout"),
    path("register/", RegisterClientView.as_view(), name="register"),
]
