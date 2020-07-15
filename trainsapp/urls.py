from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('carriages/', views.carriage_list),
    path('lineplatforms/', views.lineplatform_list),
    path('connections/', views.connection_list),
    path('buy/', views.buy_ticket),
]
