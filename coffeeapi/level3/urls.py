from django.urls import path, re_path

from coffeeapi.level3 import views

urlpatterns = [
    re_path(r'v3/receipt(?:/(?P<id>\d+))?', views.receipt),
    re_path(r'v3/payment(?:/(?P<id>\d+))?', views.payment),
    re_path(r'v3/order(?:/(?P<id>\d+))?', views.dispatch, name="order_v3"),
    #path('order', views.dispatch),
]
