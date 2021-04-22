from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def signup(requests):
    if requests.method == 'POST':
        form = UserCreationForm(requests.POST)
        if form.is_valid():
            form.save()
            # redirect(home)
    return render(requests, 'signup.html', {'form':UserCreationForm})
    
def login(requests):
    return render(requests, 'login.html')