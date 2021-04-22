from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm 
from django.contrib.auth import login as authlogin, logout as authlogout, authenticate 
from django.contrib.auth.decorators import login_required

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'signup.html', {'form':UserCreationForm})
    
def login(request):
    if request.method == 'POST':
        username = request.POST.get('your_name')
        password = request.POST.get('your_pass')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            authlogin(request, user)
            return redirect('dashboard')

    return render(request, 'login.html')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')

def logout(request):
    authlogout(request)
    return redirect('login')