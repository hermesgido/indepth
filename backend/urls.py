from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from backend import views, roles

urlpatterns = [
    # Dashboard and Authentication
    path('dashboard/', views.index, name="index"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.logout_user, name="logout_user"),

    # Customers
    path('customers/', views.customers, name="customers"),
    path('kvp-customers/', views.kvp_customers, name="kvp_customers"),
    path('kvp_pins/', views.kvp_pins, name="kvp_pins"),
    path('assign-pin/<int:pin_id>/', views.assign_pin_to_customer,
         name='assign_pin_to_customer'),


    # Staff and Facilities
    path('staff/', views.staff, name="staff"),
    path('facilities/', views.facilities, name="facilities"),
    path('facilities/edit/<str:facility_id>/',
         views.edit_facility, name='edit_facility'),
    path('facilities/delete/<int:facility_id>/',
         views.delete_facility, name='delete_facility'),

    # Roles and Permissions
    path('roles/', views.roles, name="roles"),
    path('roles/add/', roles.add_role, name='add_role'),
    path('roles/edit/<int:role_id>/', roles.edit_role, name='edit_role'),
    path('roles/delete/<int:role_id>/', roles.delete_role, name='delete_role'),
    path('roles/assign/<int:role_id>/',
         roles.assign_permissions, name='assign_permissions'),
    path('permissions/', views.permissions, name="permissions"),

    # Logs
    path('audit-logs/', views.audit_logs, name="audit_logs"),

    # Machines and Slots
    path('machines/', views.mashines, name="mashines"),
    path('machine_details/<str:id>/',
         views.machine_details, name="machine_details"),
    path('edit-slot/', views.edit_slot, name="edit_slot"),

    # Products
    path('products/', views.products, name="products"),

    # Transactions
    path('transactions/', views.transactions, name="transactions"),
    path('transactions_logs/', views.transactions_logs, name="transactions_logs"),
    path('transactions_logs/<str:id>/',
         views.transactions_logs, name="transactions_logs"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
