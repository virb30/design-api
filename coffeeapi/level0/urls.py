from django.urls import path

from .views import barista

urlpatterns = [
    path('PlaceOrder', barista),
]
