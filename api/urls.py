
from django.urls import path
from api.views import CustomerAPIView, CustomerCreateAPIView, HelloWorldView, MachineSlotsAPIView, TransactionCreateAPIView, VendingMashineCallBackAPI
from backend import views

urlpatterns = [
    # path('api/', views.home, name="home"),
    path('hello/', HelloWorldView.as_view(), name='hello-world'),
    path('customer/<str:phone_number>/', CustomerAPIView.as_view(), name='customer-detail'),
    path('customer-create/', CustomerCreateAPIView.as_view(), name='customer-create'),
    path('transaction/create/', TransactionCreateAPIView.as_view(),
         name='transaction-create'),
    path('vending/', VendingMashineCallBackAPI.as_view(), name='vending-machine-callback'),
    path('machine-slots/<str:machine_id>', MachineSlotsAPIView.as_view(), name='machine-slots')
]
