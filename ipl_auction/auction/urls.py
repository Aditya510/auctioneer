from django.urls import path
from . import views

urlpatterns = [
    path('', views.setup, name='setup'),
    path('auction/', views.auction, name='auction'),
    path('results/', views.results, name='results'),
] 