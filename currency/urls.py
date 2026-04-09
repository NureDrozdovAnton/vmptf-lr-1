from django.urls import path
from . import views

urlpatterns = [
    path('', views.currencies, name='currencies'),
    path('create/', views.create_currency, name='create_currency'),
    path('api/currencies/', views.currencies_api, name='currencies_api'),
]
