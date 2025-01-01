from backend.helpers import assign_pin, generate_kvp_pins
from .models import KvpGroup, KvpPin, Slot
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from backend.filters import CustomerFilter
from .forms import FacilityForm  
from .models import Customer, Facility, Machine, Slot, Transaction, TransactionLog
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
    customers = Customer.objects.all().count()
    transactions = Transaction.objects.all().count()
    machines = Machine.objects.all().count()
    
    context = {
        'customers': customers,
        'transactions': transactions,
        'machines': machines,
    }
    
    
    
    return render(request, 'index.html', context)


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


def transactions_logs(request, id=None):
    if id is not None:
        txn  = Transaction.objects.get(id=id)
        transaction_logs_list = TransactionLog.objects.filter(transaction=txn)
    else:
        transaction_logs_list = TransactionLog.objects.all()
    
    
    context = {"transaction_logs": transaction_logs_list}
    return render(request, 'transactions_logs.html', context)

def kvp_customers(request):
    customer_filter = CustomerFilter(
        request.GET, queryset=Customer.objects.all())
    context = {
        "filter": customer_filter,
        "customers": customer_filter.qs,
    }
    return render(request, 'kvp_customers.html', context)


def kvp_pins(request):
    facilities = Facility.objects.all()
    pins = KvpPin.objects.all().order_by('-created_at')
    groups = KvpGroup.objects.all()
    if request.method == 'POST':
        facility_id = request.POST.get('facility')
        amount  = request.POST.get('amount')
        groups = request.POST.getlist('group') 
        if not facility_id:
            messages.error(request, "Please select a facility")
            return redirect(request.META.get('HTTP_REFERER'))
        if not amount:
            messages.error(request, "Please enter the amount of pins to generate")
            return redirect(request.META.get('HTTP_REFERER'))
        if not groups:
            messages.error(request, "Please select at least one group")
            return redirect(request.META.get('HTTP_REFERER'))
        generate_kvp_pins(facility_id, amount, groups)
        return redirect(request.META.get('HTTP_REFERER'))
    
    context = {
        'facilities': facilities,
        'pins': pins,
        'groups': groups,
    }
    return render(request, 'kvp_pins.html', context)


def assign_pin_to_customer(request, pin_id):
    assign_pin(request, pin_id)
    return redirect(request.META.get('HTTP_REFERER'))

    
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
    machines_list = Machine.objects.all()
    
    context = {
       'machines': machines_list, 
    }
    return render(request, 'mashines.html', context)


def machine_details(request, id):
    machine = Machine.objects.get(id=id)
    slots = Slot.objects.filter(machine=machine)

    context = {
        'machines': machine,
        'slots': slots,
    }
    return render(request, 'mashine_details.html', context)


def edit_slot(request):
    if request.method == "POST":
        slot_id = request.POST.get("slot_id")
        slot = get_object_or_404(Slot, id=slot_id)
        slot.name = request.POST.get("name")
        slot.slot_number = request.POST.get("slot_number")
        slot.product_type = request.POST.get("product_type")
        slot.capacity = request.POST.get("capacity")
        slot.quantity_available = request.POST.get("quantity_available")
        slot.price = request.POST.get("price")
        if 'product_image' in request.FILES:
            print("Product image foundd")
            slot.product_image = request.FILES['product_image']
        slot.save()
        return redirect(request.META.get('HTTP_REFERER'))
