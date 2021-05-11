from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth import login as authlogin, logout as authlogout, authenticate
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework import status
from .decorators import allowed_users

from .serializer import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    return render(request, "signup.html", {"form": UserCreationForm})


def login(request):
    if request.method == "POST":
        username = request.POST.get("your_name")
        password = request.POST.get("your_pass")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            authlogin(request, user)
            return redirect("dashboard")

    return render(request, "login.html")

@api_view(['POST'])
def api_logout(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@login_required(login_url="login")
@allowed_users(allowed_roles=["authority"])
def dashboard(request):
    data = {"cam1": {"camera_id": 0, "location": "null", "count": 0}}
    context = {"data": data, "headers": ["camera_id", "location", "count"]}
    return render(request, "dashboard.html", context)


def logout(request):
    authlogout(request)
    return redirect("login")




class RegisterClientView(APIView):
    def get(self, format=None):

        full_client_model = Client.objects.all()
        serializer = ExtraFieldSerializer(full_client_model, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = ExtraFieldSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
