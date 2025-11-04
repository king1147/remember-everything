from django.urls import path
from . import views

urlpatterns = [
    path('', views.calculate_input, name='calculate_input'),
    path('result/', views.calculate_results, name='calculate_results'),
]