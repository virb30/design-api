from django.urls import path, re_path

from coffeeapi.level3 import views

urlpatterns = [
    re_path(r'v3/order(?:/(?P<id>\d+))?', views.dispatch, name='orderv3'),
    path('v3/receipt/<int:id>', views.receipt, name='receipt'),
    path('v3/payment/<int:id>', views.payment, name='payment'),
    #path('order', views.dispatch),
]
