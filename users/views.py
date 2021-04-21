from django.shortcuts import render

# Create your views here.
def signup(requests):
    return render(requests, 'signup.html')
    
def login(requests):
    return render(requests, 'login.html')