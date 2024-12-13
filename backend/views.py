from backend.filters import CustomerFilter
from .forms import FacilityForm  
from .models import Customer, Facility, Transaction
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from backend.models import Facility
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
    customer_filter = CustomerFilter(
        request.GET, queryset=Customer.objects.all())
    context = {
        "filter": customer_filter,
        "customers": customer_filter.qs,
    }
    return render(request, 'customers.html', context)
    

def products(request):

    return render(request, 'products.html')


def transactions(request):
    transaction_list = Transaction.objects.all()
    
    context = {"transactions": transaction_list}
    return render(request, 'transactions.html', context)

def kvp_customers(request):
    customer_filter = CustomerFilter(
        request.GET, queryset=Customer.objects.all())
    context = {
        "filter": customer_filter,
        "customers": customer_filter.qs,
    }

    return render(request, 'kvp_customers.html', context)
    
def staff(request):

    return render(request, 'staff.html')

def facilities(request):
    facilities_list = Facility.objects.all()
    
    
    context = {
        'facilities': facilities_list, 
    }
    return render(request, 'facilities.html', context)


# Edit Facility

def edit_facility(request, facility_id):
    facility = get_object_or_404(Facility, id=facility_id)
    if request.method == 'POST':
        form = FacilityForm(request.POST, instance=facility)
        if form.is_valid():
            form.save()
            # Redirect back to the facilities list
            return redirect('facilities')
    else:
        form = FacilityForm(instance=facility)

    return render(request, 'edit_facility.html', {'form': form, "facility": facility})

# Delete Facility
def delete_facility(request, facility_id):
    facility = get_object_or_404(Facility, id=facility_id)
    if request.method == 'POST':
        facility.delete()
        return redirect('facilities')  # Redirect back to the facilities list

    return render(request, 'confirm_delete.html', {'facility': facility})


def roles(request):

    return render(request, 'roles.html')
def permissions(request):

    return render(request, 'permissions.html')
def audit_logs(request):

    return render(request, 'audit_logs.html')


def mashines(request):
    return render(request, 'mashines.html')