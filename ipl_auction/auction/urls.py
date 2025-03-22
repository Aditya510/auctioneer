from django.urls import path
from . import views

urlpatterns = [
    path('', views.results, name='results'),
    path('setup/', views.setup, name='setup'),
    path('auction/', views.auction, name='auction'),
] 