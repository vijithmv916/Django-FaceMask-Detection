from django.urls import path
# from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    signup,
    login,
    dashboard,
    logout,
    RegisterClientView,
    api_logout,
    CustomAuthToken
)

urlpatterns = [
    path("", signup, name="signup"),
    path("login/", login, name="login"),
    path("dashboard/<str:username>", dashboard, name="dashboard"),
    path("logout/", logout, name="logout"),
    path("register/", RegisterClientView.as_view(), name="register"),
    path("APILogin/", CustomAuthToken.as_view(), name='APILogin'),
    path('APILogout/', api_logout, name='APILogout')
]
