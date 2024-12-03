from django.contrib import admin

from backend.models import Customer, Machine, Slot, Transaction

# Register your models here.
admin.site.register(Customer)
admin.site.register(Transaction)
admin.site.register(Machine)
admin.site.register(Slot)