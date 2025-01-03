# from django.contrib import admin

# from backend.models import Customer, Machine, Slot, Transaction

# # Register your models here.
# admin.site.register(Customer)
# admin.site.register(Transaction)
# admin.site.register(Machine)
# admin.site.register(Slot)


from django.contrib import admin
from django.utils.html import format_html
from .models import AppUpdate, Facility, KvpGroup, KvpPin, Machine, MachineLogs, Slot, Customer, Transaction, TransactionLog


class MachineAdmin(admin.ModelAdmin):
    list_display = ('name', 'machine_id', 'location', 'status', 'description')
    search_fields = ('name', 'machine_id', 'location')
    list_filter = ('status', 'location')



class FacilityAdmin(admin.ModelAdmin):
    list_display  = ('district', 'ward', 'supporting_facility', 'responsible_cso',
                     'responsible_person', 'mobile_no', 'app_password', 'status', 'created_at', 'updated_at')
    search_fields =('district', 'ward', 'supporting_facility', 'responsible_cso',
                    'responsible_person', 'mobile_no', 'app_password', 'status')
    list_filter =('district', 'ward', 'supporting_facility', 'responsible_cso',
                  'responsible_person', 'mobile_no', 'app_password', 'status')




class SlotAdmin(admin.ModelAdmin):
    list_display = ('name', 'slot_number', 'machine', 'product_type',
                    'capacity', 'quantity_available', 'price', 'created_at', 'updated_at')
    search_fields = ('name', 'slot_number', 'machine__name', 'product_type')
    list_filter = ('product_type', 'machine__name', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

    def machine_name(self, obj):
        return obj.machine.name


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'location',
        'type',
        'client_group',
        'phone_number',
        'age',
        'gender',
        'registered_machine',
        'condom_transaction_limit',
        'kits_transaction_limit',
        'today_condom_transactions',
        'today_kits_transactions',
    )
    search_fields = ('name', 'location', 'phone_number',
                     'registered_machine__name')
    list_filter = ('type', 'client_group', 'gender')
   

    def registered_machine_name(self, obj):
        return obj.registered_machine.name if obj.registered_machine else None


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'customer',
        'machine',
        'amount',
        'slot',
        'product_type',
        'status',
        'created_at',
        'updated_at',
    )
    search_fields = ('customer__name', 'machine__name',
                     'slot__name', 'product_type')
    list_filter = ('product_type', 'status', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


class TransactionLogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'transaction',
        'machine',
        'slot',
        'product_type',
        'status',
        'created_at',
        'updated_at'
    )
    list_filter = ('product_type', 'status', 'created_at') 
    search_fields = ('trade_number', 'status')  
    ordering = ('-created_at',)  
    readonly_fields = ('created_at', 'updated_at')



# Registering models to the admin
admin.site.register(Machine, MachineAdmin)
admin.site.register(Slot, SlotAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(TransactionLog, TransactionLogAdmin)
admin.site.register(MachineLogs)
admin.site.register(AppUpdate)
admin.site.register(KvpGroup)
admin.site.register(KvpPin)



# Customizing Admin Dashboard
admin.site.site_header = "Transaction Management System"
admin.site.site_title = "TMS Admin Dashboard"
admin.site.index_title = "Welcome to the Transaction Management System Admin Panel"
