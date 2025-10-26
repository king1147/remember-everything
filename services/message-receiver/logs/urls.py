from django.urls import path
from . import views

urlpatterns = [
    path('logs/', views.log_viewer, name='log_viewer'),
]