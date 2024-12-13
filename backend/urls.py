
from django.urls import path
from backend import views
from backend import roles

urlpatterns = [
    path('dashboard/', views.index, name="index"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.logout_user, name="logout_user"),
    path('customers/', views.customers, name="customers"),
    path('kvp-customers/', views.kvp_customers, name="kvp_customers"),
    path('staff/', views.staff, name="staff"),
    path('facilities/', views.facilities, name="facilities"),
    path('facilities/edit/<str:facility_id>/',
         views.edit_facility, name='edit_facility'),

    path('facilities/delete/<int:facility_id>/',
         views.delete_facility, name='delete_facility'),


    path('roles/', views.roles, name="roles"),
    path('roles/add/', roles.add_role, name='add_role'),
    path('roles/edit/<int:role_id>/', roles.edit_role, name='edit_role'),
    path('roles/delete/<int:role_id>/', roles.delete_role, name='delete_role'),
    path('permissions', views.permissions, name="permissions"),
    path('roles/assign/<int:role_id>/',
         roles.assign_permissions, name='assign_permissions'),
    path('audit-logs', views.audit_logs, name="audit_logs"),

    path('mashines/', views.mashines, name="mashines"),
    path('products/', views.products, name="products"),
    
    path('transactions/', views.transactions, name="transactions"),
    path('transactions_logs/', views.transactions_logs, name="transactions_logs"),
    path('transactions_logs/<str:id>/',
         views.transactions_logs, name="transactions_logs")

]
