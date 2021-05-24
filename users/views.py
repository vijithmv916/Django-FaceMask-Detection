from typing import Container
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth import login as authlogin, logout as authlogout, authenticate
from django.contrib.auth.decorators import login_required
from django.template import context
from rest_framework import response
from rest_framework.decorators import api_view
from rest_framework import status
from .decorators import allowed_users
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializer import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import requests
from bs4 import BeautifulSoup as b




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
            return redirect(f"http://127.0.0.1:8000/dashboard/{username}")

    return render(request, "login.html")


@api_view(["POST"])
def api_logout(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        # get client user
        c_user = Token.objects.get(key=token.key).user
        cli = Client.objects.get(user=c_user)

        return Response({
            'token': token.key,
            'authority': cli.authority,
        })

@login_required(login_url="login")
@allowed_users(allowed_roles=["authority"])
def dashboard(request, username):

    authority_code = User.objects.get(username=username)

    client_user = Client.objects.filter(authority=username)


    context = {"authority_code": authority_code, "c_users": client_user}

    # data = {"cam1": {"camera_id": 0, "location": "null", "count": 0}}
    # context = {"data": data, "headers": ["camera_id", "location", "count"]}
    return render(request, "dashboard.html", context)


# covid page
@login_required(login_url="login")
@allowed_users(allowed_roles=["authority"])

def covid(request):

    url = 'https://dashboard.kerala.gov.in/daily.php'
    html_data = requests.get(url).text
    name = b(html_data)
    my_list = name.find_all('h3', {'class':'my-lg-1'})

    today_pos = my_list[0].text.split('(')
    admitts = my_list[1].text.split('(')
    neg = my_list[2].text.split('(')
    death = my_list[3].text.split('(')
    context = {
        'today':today_pos[0],
        'today_udt':today_pos[1][:-1],
        'admited':admitts[0],
        'admited_udt':admitts[1][:-1],
        'negative':neg[0],
        'negative_udt':neg[1][:-1],
        'death':death[0],
        'death_udt':death[1][:-1],
    }

    return render(request, "covid.html", context)


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
