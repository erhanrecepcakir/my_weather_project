from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,"index.html")

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email   = form.cleaned_data.get('email')

        newUser = User(username = username, email = email)
        newUser.set_password(password)
        newUser.save()
        login(request, newUser)
        messages.info(request, 'Registeration is successful')

        return redirect('index')
    context = {
        'form' : form
    }
    return render(request, "register.html", context)

def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        'form' : form
    }
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.warning(request, "Login process is not authenticated. Please check login info..")
            return render(request, 'login.html',context)
        messages.info(request, "Login process is successful")
        login(request,user)
        return redirect('index')
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    messages.info(request, "Logout process is successful")
    return redirect('index')
