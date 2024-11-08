from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.


@login_required
def index(request):
    
    
    return render(request, 'index.html')


def logout_user(request):
    logout(request)
    return redirect(index)


def user_login(request):
    if request.method == 'POST':
        print("ddddddddd")

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        print("ddddddddd")

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'auth/login.html')


def customers(request):
    
    return render(request, 'customers.html')

def products(request):

    return render(request, 'products.html')


def kvp_customers(request):

    return render(request, 'kvp_customers.html')

def staff(request):

    return render(request, 'staff.html')

def roles(request):

    return render(request, 'roles.html')
def permissions(request):

    return render(request, 'permissions.html')
def audit_logs(request):

    return render(request, 'audit_logs.html')


def mashines(request):
    return render(request, 'mashines.html')