
from django.urls import path
from api.views import AdminLogin, CustomerAPIView, CustomerCreateAPIView, HelloWorldView, MachineSlotsAPIView, SetMachineIdAndPassword, TransactionCreateAPIView, VendingMashineCallBackAPI, check_app_update
from backend import views
urlpatterns = [
    # path('api/', views.home, name="home"),
    path('hello/', HelloWorldView.as_view(), name='hello-world'),
    path('customer/<str:phone_number>/', CustomerAPIView.as_view(), name='customer-detail'),
    path('customer-create/', CustomerCreateAPIView.as_view(), name='customer-create'),
    path('transaction-create/', TransactionCreateAPIView.as_view(),
         name='transaction-create'),
    path('vending/', VendingMashineCallBackAPI.as_view(), name='vending-machine-callback'),
    path('machine-slots/<str:machine_id>', MachineSlotsAPIView.as_view(), name='machine-slots'),
    path('machine-slots/',
         MachineSlotsAPIView.as_view(), name='machine-slots'),

    path('machine-login/', SetMachineIdAndPassword.as_view(), name="machine-login"),
    path('admin-login/', AdminLogin.as_view(), name="admin-login"),
    path('check-app-update/', check_app_update, name='check-app-update'),

]
