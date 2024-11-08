
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
    
    
    path('roles/', views.roles, name="roles"),
    path('roles/add/', roles.add_role, name='add_role'),
    path('roles/edit/<int:role_id>/', roles.edit_role, name='edit_role'),
    path('roles/delete/<int:role_id>/', roles.delete_role, name='delete_role'),
    path('permissions', views.permissions, name="permissions"),
    path('roles/assign/<int:role_id>/', roles.assign_permissions, name='assign_permissions'),
    path('audit-logs', views.audit_logs, name="audit_logs"),
    
    path('mashines/', views.mashines, name="mashines"),
    path('products/', views.products, name="products"),
    
]
