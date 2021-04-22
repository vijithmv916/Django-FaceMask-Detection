from django.urls import path
from .views import (
    signup,
    login,
    dashboard
)

urlpatterns = [
    path('', signup, name='signup'),
    path('login/', login, name='login'),
    path('dashboard/', dashboard, name='dashboard')
]