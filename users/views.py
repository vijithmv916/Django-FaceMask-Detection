from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
# from .form import Custom_name
from django.forms import ModelForm 

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # redirect(home)
    return render(request, 'signup.html', {'form':UserCreationForm})
    
def login(request):
    return render(request, 'login.html')