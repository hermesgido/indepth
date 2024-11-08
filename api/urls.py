
from django.urls import path
from api.views import HelloWorldView
from backend import views

urlpatterns = [
    # path('api/', views.home, name="home"),
    path('hello/', HelloWorldView.as_view(), name='hello-world'),

]
