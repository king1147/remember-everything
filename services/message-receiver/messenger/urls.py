from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='send_message', permanent=False)),
    path('send/', views.send_message, name='send_message'),
]